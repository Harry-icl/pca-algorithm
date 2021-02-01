import numpy as np
import sys, requests
import json
import pandas as pd


from .total_funds import calculate_funds


def create(new_proportions: pd.DataFrame, portfolio, cash) -> "list(dict)":
    """
    Function to create a set of orders based on the current portfolio and the required portfolio.

    Parameters:
        new_proportions (pd.DataFrame): the new proportions required
    
    Returns:
        list(dict): a list of orders to execute
    """

    # Make mechanism for negative proportions

    total_funds_95 = 0.95*calculate_funds(portfolio, cash)
    orders = []
    for epic, row in new_proportions.iterrows():
        new = row[0]
        if portfolio['position.size'][epic] >= 0:
            cur = (portfolio['Open'][epic] * portfolio['position.size'][epic]) / total_funds_95
            if new - cur > 0.05:
                min_n = np.floor((new-cur)*total_funds_95/portfolio['Open'][epic])
                max_n = np.ceil((new-cur)*total_funds_95/portfolio['Open'][epic])
                if abs(cur + portfolio['Open'][epic]*min_n/total_funds_95 - new) < abs(cur + portfolio['Open'][epic]*max_n/total_funds_95 - new):
                    orders.append({'epic': epic, 'size': min_n, 'type': 'BUY'})
                else:
                    orders.append({'epic': epic, 'size': max_n, 'type': 'BUY'})

            elif cur - new > 0.05:
                min_n = np.floor((cur-new)*total_funds_95/portfolio['Open'][epic])
                max_n = np.ceil((cur-new)*total_funds_95/portfolio['Open'][epic])
                if abs(cur - portfolio['Open'][epic]*min_n/total_funds_95 - new) < abs(cur - portfolio['Open'][epic]*max_n/total_funds_95 - new):
                    orders.append({'epic': epic, 'size': min_n, 'type': 'SELL'})
                else:
                    orders.append({'epic': epic, 'size': max_n, 'type': 'SELL'})

        else:
            cur = (portfolio['position.size'][epic] / portfolio['Open'][epic]) / total_funds_95
            if new - cur > 0.05:
                min_n = np.floor((new-cur)*total_funds_95*portfolio['Open'][epic])
                max_n = np.ceil((new-cur)*total_funds_95*portfolio['Open'][epic])
                if abs(cur + min_n/(portfolio['Open'][epic]*total_funds_95) - new) < abs(cur + max_n/(portfolio['Open'][epic]*total_funds_95) - new):
                    orders.append({'epic': epic, 'size': min_n, 'type': 'BUY'})
                else:
                    orders.append({'epic': epic, 'size': max_n, 'type': 'BUY'})

            elif cur - new > 0.05:
                min_n = np.floor((cur-new)*total_funds_95*portfolio['Open'][epic])
                max_n = np.ceil((cur-new)*total_funds_95*portfolio['Open'][epic])
                if abs(cur - min_n/(portfolio['Open'][epic]*total_funds_95) - new) < abs(cur - max_n/(portfolio['Open'][epic]*total_funds_95) - new):
                    orders.append({'epic': epic, 'size': min_n, 'type': 'SELL'})
                else:
                    orders.append({'epic': epic, 'size': max_n, 'type': 'SELL'})
    return orders

def create_cont(new_proportions: pd.DataFrame, portfolio, cash) -> "list(dict)":
    """
    Function to create a set of orders based on the current portfolio and the required portfolio.

    Parameters:
        new_proportions (pd.DataFrame): the new proportions required
    
    Returns:
        list(dict): a list of orders to execute
    """


    total_funds_95 = 0.95*calculate_funds(portfolio, cash)
    orders = []
    for epic, row in new_proportions.iterrows():
        new = row[0]
        if portfolio['position.size'][epic] >= 0:
            cur = (portfolio['Open'][epic] * portfolio['position.size'][epic]) / total_funds_95
            if new - cur > 0:
                size = (new-cur)*total_funds_95/portfolio['Open'][epic]
                orders.append({'epic': epic, 'size': size, 'type': 'BUY'})

            elif cur - new > 0:
                size = (cur-new)*total_funds_95/portfolio['Open'][epic]
                orders.append({'epic': epic, 'size': size, 'type': 'SELL'})

        else:
            cur = (portfolio['position.size'][epic]*portfolio['Open'][epic]) / total_funds_95
            if new - cur > 0:
                size = (new-cur)*total_funds_95/portfolio['Open'][epic]
                orders.append({'epic': epic, 'size': size, 'type': 'BUY'})

            elif cur - new > 0:
                size = (cur-new)*total_funds_95/portfolio['Open'][epic]
                orders.append({'epic': epic, 'size': size, 'type': 'SELL'})
    return orders