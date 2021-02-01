import pandas as pd
import numpy as np

from .data import Data, DataType
from .choose_stocks import choose
from .backtest_execute import execute_trades
from .backtest_create_order import create, create_cont
from .constants import stock_list
from .total_funds import calculate_funds

def backtest(period: int, starting_cash: float, filepath: str, baseline: bool = False, baseline_index: int = None):
    record = {}
    raw_data = pd.read_csv(filepath)
    print(raw_data)
    full_data = {x: Data(DataType.historical, raw_data.pivot(index='Date', columns='Epic', values=x)) for x in ['High', 'Low', 'Open', 'Close']}

    for x in ['High', 'Low', 'Open', 'Close']:
        full_data[x].data.index = pd.to_datetime(full_data[x].data.index, format="%d/%m/%Y %H:%M") # change back if not doing hourly anymore
        full_data[x].data.sort_index(inplace=True)
        full_data[x].data.dropna(inplace=True, axis=0)
        full_data[x].data = full_data[x].data.astype(np.float64)

    print(full_data['High'].data)
    print("PERIOD %s RUNNING" % period)
    record = pd.DataFrame(columns=["Date", "Portfolio Value"])
    portfolio = pd.DataFrame(columns = ['High', 'Low', 'Open', 'Close', 'position.size'], index=full_data['Open'].data.columns)
    cash = starting_cash
    portfolio['position.size'].values[:] = 0
    portfolio.index.name = 'market.epic'
    for j in range(period, len(full_data['High'].data)):
        small_data = {x: Data(DataType.historical, full_data[x].data.iloc[j-period:j]) for x in ['High', 'Low', 'Open', 'Close']}
        pca_data = small_data['Open'].PCA()
        for epic, _ in portfolio.iterrows():
            for x in ['High', 'Low', 'Open', 'Close']:
                portfolio.loc[epic, x] = small_data[x].data.iloc[len(small_data[x].data) - 1][epic]
        if baseline:
            diff = [0]*len(portfolio)
            diff[baseline_index] = 1
            new_proportions = pd.DataFrame(diff, index=pca_data.data.columns)
        else:
            new_proportions = choose(small_data['Open'], pca_data)
        orders = create_cont(new_proportions, portfolio, cash)
        portfolio, cash = execute_trades(orders, portfolio, cash)
        portfolio_value = calculate_funds(portfolio, cash)
        record = record.append({"Date": small_data['Open'].data.index[-1], "Portfolio Value": portfolio_value}, ignore_index=True)
        print(portfolio)
        print("Cash: %s; Portfolio Value: %s" % (cash, portfolio_value))
    
    return record