import requests, sys, json
import pandas as pd


from .constants import currency

#TODO: Place StreamClient Class from ig2.py into this file.
#TODO: Verify get_historical_data works and dataframe is correctly formatted.
#TODO: Synthesis of RestClient & StreamClient into a working module

class RestClient:
    """
    Class for completing REST API actions. Always login before the request and logout afterwards - unless repeated requests will be made, in which case log in, complete all requests, then logout, for speed.

    Attributes:
        api_key (str): the API key to use for login
        identifier (str): the identifier to use
        password (str): the password to use for login
        url (str): the URL to send HTTP requests to
        xst (str): the security token
        cst (str): the CST to use
    """

    def __init__(self, rest_api_key: str, rest_identifier: str, rest_password: str, rest_url: str) -> None:
        """
        Constructor for the RestClient class.

        Parameters:
            rest_api_key (str): the API key to use for login
            rest_identifier (str): the identifier to use
            rest_password (str): the password to use for login
            rest_url (str): the URL to send HTTP requests to
        """
        
        self.api_key = rest_api_key
        self.identifier = rest_identifier
        self.password = rest_password
        self.url = rest_url


    def _get_request_df(self, name, url, headers, request_json) -> pd.DataFrame:
        """
        Function to return a dataframe from an HTTP GET request.

        Parameters:
            name (str): the type of data being requested
            url (str): the url to send the HTTP request to
            headers (dict): the headers to send with the HTTP request
            json (dict): the json content to send with the HTTP request
        
        Returns:
            pd.DataFrame: the data in a pandas DataFrame.
        """

        response = requests.request("GET", url, headers=headers, json=request_json)

        if response.status_code != 200:
            print("error\n", response.status_code, url, response.text)
            sys.exit(0)
        response_df = pd.io.json.json_normalize(json.loads(response.content)[name])

        return response_df
    

    def login(self) -> None:
        """
        Function to login to the session.
        """

        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json; charset=UTF-8",
            "Version": "2",
            "X-IG-API-KEY": self.api_key,
        }
        request_json = {
            "identifier": self.identifier,
            "password": self.password,
        }

        rest_response = requests.request("POST", self.url + '/session', headers=headers, json=request_json)
        if rest_response.status_code != 200:
            print("error", rest_response.status_code, self.url + '/session', rest_response.text)
            sys.exit(0)
        
        self.xst = rest_response.headers["X-SECURITY-TOKEN"]
        self.cst = rest_response.headers["CST"]


    def logout(self) -> None:
        """
        Function to logout of the session.
        """

        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json; charset=UTF-8",
            "Version": "1",
            "X-IG-API-KEY": self.api_key,
            "X-SECURITY-TOKEN": self.xst,
            "CST": self.cst,
        }
        request_json = {}
        rest_response = requests.request("DELETE", self.url + '/session', headers=headers, json=request_json)

        if rest_response.status_code != 204:
            print("error", rest_response.status_code, self.url + '/session', rest_response.text)
            sys.exit(0)
    
    
    def get_historical_data(self, epic: str, resolution : str, startDate : str, endDate : str) -> pd.DataFrame:

        """
        -------------------------------------------------------------------------------------
        INPUTS:
        
        epic = shortcode for a particular instrument in form IX.D.DOW.DAILY.IP:
            e.g. 'CC.D.FGBL.UME.IP'
        
        IX.D.DOW.DAILY.IP:.

        IX = method – IX is the method for ‘Index Out of Hours’ – each asset type will have it’s own method
        D – all our trade-able epics will have D here
        DOW = underlying – this is generally the underlying market
        DAILY = option – this indicates a different method of processing the underlying data – in this case a daily funded bet
        IP – this bit will always be IP for all our trade-able epics

        resolution = denotion of intervals of historical prices
            e.g. 'DAY'

        startDate = the startdate of the historical data requested, in format 'YYYY-MM-DD'

        endDate = the enddate of the historical data requested, in format 'YYYY-MM-DD'
        -------------------------------------------------------------------------------------
        OUTPUTS: v0.9

        (json format) all available data regarding prices for the time interval provided.
        """

        _EPIC = epic
        _RESOLUTION = resolution
        _STARTDATE = startDate
        _ENDDATE = endDate
        _URL = self.url + "/prices"

        #REQUIRED: Set version to 3
        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json; charset=UTF-8",
            "Version": "3",
            "X-IG-API-KEY": self.api_key,
            "X-SECURITY-TOKEN": self.xst,
            "CST": self.cst,
        }
        url_hprices = _URL + "/%s?resolution=%s&from=%s&to=%s&pageSize=0" % (_EPIC, _RESOLUTION, _STARTDATE, _ENDDATE)
        request_json = {}

        req_data = "prices"

        return self._get_request_df(req_data, url_hprices, headers, request_json)

    def get_positions(self) -> pd.DataFrame:
        """
        Function that returns the currently held positions in a pandas DataFrame.
        
        Returns:
            pd.DataFrame: current positions
        """

        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json; charset=UTF-8",
            "Version": "2",
            "X-IG-API-KEY": self.api_key,
            "X-SECURITY-TOKEN": self.xst,
            "CST": self.cst,
        }
        request_json = {}
        url = self.url + '/positions'

        return self._get_request_df('positions', url, headers, request_json)

    
    def get_accounts(self) -> pd.DataFrame:
        """
        Function that returns the details of the current account.

        Returns:
            pd.DataFrame: account details
        """

        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json; charset=UTF-8",
            "Version": "1",
            "X-IG-API-KEY": self.api_key,
            "X-SECURITY-TOKEN": self.xst,
            "CST": self.cst,
        }
        request_json = {}
        url = self.url + '/accounts'

        return self._get_request_df('accounts', url, headers, request_json)


    def get_prices(self, epic) -> pd.DataFrame:
        """
        Function that returns the current prices of the given epic.

        Parameters:
            epic (str): the epic for the stock whose prices to fetch
        
        Returns:
            pd.DataFrame: the various prices - bid, offer, etc. for the given epic
        """

        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json; charset=UTF-8",
            "Version": "3",
            "X-IG-API-KEY": self.api_key,
            "X-SECURITY-TOKEN": self.xst,
            "CST": self.cst,
        }
        request_json = {}
        url = self.url + '/markets/' + epic
        
        return self._get_request_df('snapshot', url, headers, request_json)


    def execute_trade(self, epic, size, trade_type) -> str:
        """
        Function that buys the required amount of the stock.

        Parameters:
            epic (str): the epic for the stock to buy
            size (int): the size of the order

        Returns:
            str: the deal reference
        """

        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json; charset=UTF-8",
            "Version": "2",
            "X-IG-API-KEY": self.api_key,
            "X-SECURITY-TOKEN": self.xst,
            "CST": self.cst,
        }
        request_json = {
            "epic": epic,
            "expiry": "-",
            "direction": trade_type,
            "size": str(size),
            "orderType": "MARKET",
            "timeInForce": "EXECUTE_AND_ELIMINATE",
            "guaranteedStop": "false",
            "forceOpen": "false",
            "currencyCode": epic[8:11]
        }
        url = self.url + '/positions/otc'

        response = requests.request("POST", url, headers=headers, json=request_json)
        if response.status_code != 200:
            print("error", response.status_code, url, response.text)
            sys.exit(0)
        return json.loads(response.content)

    def confirm_trade(self, dealRef) -> bool:
        """
        Function that confirms whether a trade has gone through, and if not prints the error.

        Parameters:
            dealRef: the deal reference for the trade to check
        
        Returns:
            bool: confirmation of whether the trade has gone through
        """

        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json; charset=UTF-8",
            "Version": "1",
            "X-IG-API-KEY": self.api_key,
            "X-SECURITY-TOKEN": self.xst,
            "CST": self.cst,
        }
        request_json = {}
        url = self.url + '/confirms/' + dealRef

        response = requests.request("GET", url, headers=headers, json=request_json)

        if response.status_code != 200:
            print("error\n", response.status_code, url, response.text)
            sys.exit(0)
        reason = json.loads(response.content)['reason']
        if reason != 'SUCCESS':
            return False, response
        else:
            return True, response