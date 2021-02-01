from datetime import datetime
import pytz
import pandas as pd


from .rest_client import RestClient
from .stream_client import StreamClient
from .constants import *

path = "romeo-sierra/romeo_sierra/src/csv_data" #NOTE: CHANGE THIS

def get_london_time():
    tz_London = pytz.timezone('Europe/London')
    datetime_London = datetime.now(tz_London)
    return datetime_London.strftime("%H:%M:%S")

#Retrieve Historical Data
def get_historical_data(start_date, end_date, stock_list) -> "pd.DataFrame":
    rs = RestClient(rest_api_key, rest_identifier, rest_password, rest_url)
    data = pd.DataFrame(columns=[])
    data.index.name = 'snapshotTime'
    rs.login()
    for stock_ticker in stock_list:
        h_data = rs.get_historical_data(stock_ticker, "DAY", str(start_date)[:10], str(end_date)[:10])[['snapshotTime', 'openPrice.bid']]
        h_data.set_index('snapshotTime', inplace=True)
        h_data.rename(columns={'openPrice.bid': stock_ticker}, inplace=True)
        data = pd.concat([data, h_data], axis=1, sort=True)
    data.dropna(inplace=True)
    rs.logout()
    return data


#Retrieve Realtime Data
def get_realtime_stream_data(stock_ticker):
    st = StreamClient(rest_api_key, rest_identifier, rest_password, rest_url)
    st.login()
    st.ig_streaming_login()
    st.subscribe(item='MARKET', epic=stock_ticker, field='BID', data_pts = 3)
    st.logout()


#TODO: 30th Jan Add CSV Functionality


