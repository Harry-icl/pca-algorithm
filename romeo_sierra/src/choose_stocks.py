import pandas as pd
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

from .data import Data

fee = 0

def incfunc(y, cur):
    if y > cur:
        return y - cur
    else:
        return 0

def decfunc(y, cur):
    if y < cur:
        return cur - y
    else:
        return 0

def choose(original: Data, pca: Data) -> np.ndarray:
    data_differences = pca.data.sub(original.data)
    mean_diff = data_differences.mean()
    std_diff = data_differences.std()
    latest_data = original.data.iloc[-1]
    latest_pca = pca.data.iloc[-1]
    x = (latest_pca-latest_data)
    #diff = norm.cdf(x, loc=mean_diff, scale=std_diff) - norm.cdf(mean_diff-x, loc=mean_diff, scale=std_diff)
    props = [0]*len(x)
    for i in range(len(x)):
        cur = x[i]
        if cur > mean_diff[i]:
            W = norm.cdf(cur, loc=mean_diff[i], scale=std_diff[i])
            R_num = norm.expect(lambda y: cur - y, loc=100*mean_diff[i], scale=10000*std_diff[i], ub=cur)
            R_den = norm.expect(lambda y: y - cur, loc=100*mean_diff[i], scale=10000*std_diff[i], lb=cur)
            R = R_num/R_den
            props[i] = W - (1-W)/R
        elif cur < mean_diff[i]:
            W = 1 - norm.cdf(cur, loc=mean_diff[i], scale=std_diff[i])
            R_num = norm.expect(lambda y: y - cur, loc=100*mean_diff[i], scale=10000*std_diff[i], lb=cur)
            R_den = norm.expect(lambda y: cur - y, loc=100*mean_diff[i], scale=10000*std_diff[i], ub=cur)
            R = R_num/R_den
            props[i] = - (W - (1-W)/R)
    """
    for i in range(len(diff)):
        if abs(diff[i]) <= fee:
            diff[i] = 0
    diff = diff/sum(np.absolute(diff))
    if diff[0] > 0:
        diff = [1] + [0]*(len(diff) - 1)
    elif diff[0] < 0:
        diff = [-1] + [0]*(len(diff) - 1)
    else:
        diff = [0]*len(diff)
    """
    props = [props[0]] + [0]*(len(props)-1)
    return pd.DataFrame(props, index=pca.data.columns)