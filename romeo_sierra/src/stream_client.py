import requests, sys, json, csv, pytz
import pandas as pd
import numpy as np
from datetime import datetime


from .constants import currency


#TODO: Modify to improve flexibility of LS_schema and parameters in subscribe function 

class StreamClient: 

    """
    Class for completing STREAMING API actions. Always login before the request and logout afterwards - unless repeated requests will be made, in which case log in, complete all requests, then logout, for speed.

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
        Constructor for the Client class.

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

    def get_time(self, location: str):
        tz = pytz.timezone(location)
        dt = datetime.now(tz)
        return dt.strftime("%H:%M:%S")

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
        else:
            print("Connection Successful")
                
        self.xst = rest_response.headers["X-SECURITY-TOKEN"]
        self.cst = rest_response.headers["CST"]

        response_json = rest_response.json()
        self.current_account = response_json["currentAccountId"]
        self.lightstreamer_endpoint = response_json["lightstreamerEndpoint"]

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
        
    def ig_streaming_login(self) -> None:

        streaming_url = "%s/lightstreamer/create_session.txt" % (self.lightstreamer_endpoint)
        streaming_user = self.current_account
        streaming_password = "CST-{}|XST-{}".format(self.cst, self.xst)

        #TODO: Store LS_cid in constants. Unaware of how to obtain this.

        query = {
            "LS_op2": "create",
            "LS_cid": "mgQkwtwdysogQz2BJ4Ji kOj2Bg",
            "LS_user": streaming_user,
            "LS_password": streaming_password
        }

        streaming_response = requests.request("POST", streaming_url, data=query, stream=True)

        if streaming_response.status_code != 200:
            print("error", streaming_response.status_code, streaming_url, streaming_response.text)
            sys.exit(0)

        self.streaming_session = None
        self.control_domain = None
        self.streaming_iterator = streaming_response.iter_lines(chunk_size=80, decode_unicode=True)

        for line in self.streaming_iterator:
            print("line", line)
            if ":" not in line:
                continue
            [param,value] = line.split(":",1)
            if param == "SessionId":
                self.streaming_session = value
            if param == "ControlAddress":
                self.control_domain = value
            if self.streaming_session and self.control_domain:
                break

    #Opens control connection and subscribes to prescribed EPIC.
    def subscribe(self, item: str, epic: str, field: str, data_pts: int) -> None:
        control_url = "https://%s/lightstreamer/control.txt" % (self.control_domain)

        query = {}
        query["LS_session"] = self.streaming_session
        query["LS_op"] = "add"
        query["LS_table"] = "1"

        #This is specific to the market Item
        query["LS_id"] = "%s:%s" % (item.upper(),epic)

        #Place any requests you like in LS_schema. This will give required data.
        #Multiple requests may be added. This will require spaces in between each field keyword.
        query["LS_schema"] = field.upper()

        query["LS_mode"] = "MERGE"

        control_response = requests.request("POST", control_url, data=query)

        if control_response.status_code != 200:
            print("error", control_response.status_code, control_url, control_response.text)
            sys.exit(0)
        else:
            print("Connection successful. Transmitting live data now...\n")

        # Data to CSV
        tot_data = {}
        data = []
        t = []
        
        for line in self.streaming_iterator:
            if len(data) == data_pts:
                break

            if "|" in line:
                time = self.get_time('Europe/London')
                datapt = line.split('|')[1]
                print('%s: %s' % (time, datapt))

                t.append(time)
                data.append(float(datapt))

        tot_data = {'Time': t, field:data}
        print(tot_data)

        df = pd.DataFrame(tot_data)
        df.to_csv("romeo-sierra/romeo_sierra/src/csv_data/realtime_data_prices.csv", encoding='utf-8', index=False)



                









    