import pandas as pd

from .data import Data
from .choose_stocks import choose
from .execute import execute_trades
from .constants import stock_list
from .create_order import create

from .data_fetch import get_historical_data


def engine():
    data = Data.build_data(stock_list, start_date=pd.Timestamp.now()-pd.Timedelta('88 days'), end_date=pd.Timestamp.now(), historical=True)
    pca_data = data.PCA()
    new_proportions = choose(data, pca_data)
    orders = create(new_proportions)
    print(orders)
    execute_trades(orders)