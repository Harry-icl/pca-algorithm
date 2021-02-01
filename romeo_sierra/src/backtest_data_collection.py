import matplotlib.pyplot as plt

from .backtest import backtest


def collect():
    #records = [backtest(i, 1000, "C:/Users/harry/romeo-sierra/romeo_sierra/src/csv_data/Currency Prices Short.csv") for i in range(5, 200, 5)]
    #price_changes = records[1:]['Portfolio Value']/records[:-1]['Portfolio Value'] - 1
    #records = [backtest(i, 1000, "C:/Users/harry/romeo-sierra/romeo_sierra/src/csv_data/Currency Prices.csv") for i in range(5,200,5)]
    backtest_result = backtest(24, 1000, "C:/Users/harry/romeo-sierra/romeo_sierra/src/csv_data/1h Crypto Data.csv")
    baseline_result = backtest(24, 1000, "C:/Users/harry/romeo-sierra/romeo_sierra/src/csv_data/Currency Prices.csv", baseline=True, baseline_index=0)
    #for i in range(len(records)):
    #    plt.plot(records[i]["Date"], records[i]["Portfolio Value"])
    plt.plot(backtest_result["Date"], backtest_result["Portfolio Value"])
    plt.plot(baseline_result["Date"], baseline_result["Portfolio Value"])
    plt.show()
    #plt.plot(backtest_result["Date"], backtest_result["Portfolio Value"] - baseline_result["Portfolio Value"])
    #plt.show()