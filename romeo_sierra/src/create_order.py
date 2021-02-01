import numpy as np
import sys, requests
import json
import pandas as pd

from .constants import *
from .rest_client import RestClient



def create(new_proportions: pd.DataFrame) -> "list(dict)":
    """
    Function to create a set of orders based on the current portfolio and the required portfolio.

    Parameters:
        new_proportions (pd.DataFrame): the new proportions required
    
    Returns:
        list(dict): a list of orders to execute
    """

    client = RestClient(rest_api_key, rest_identifier, rest_password, rest_url)
    client.login()
    positions = client.get_positions()
    if not positions.empty:
        positions = positions[['market.epic', 'position.size', 'position.direction']]
        for i in positions.index:
            if positions['position.direction'][i] == 'SELL':
                positions['position.size'][i] = -positions['position.size'][i]
        positions.drop('position.direction', axis=1, inplace=True)
        positions.set_index('market.epic', inplace=True)
        positions = positions.groupby(positions.index).agg({'position.size': sum})
    accounts = client.get_accounts()
    total_funds_95 = accounts[accounts.accountName.isin(['CFD'])]['balance.balance'][1]*0.95
    orders = []
    for epic, row in new_proportions.iterrows():
        new = row[0]
        prices = client.get_prices(epic)
        bid = prices['bid'][0]*333
        offer = prices['offer'][0]*333
        if epic in positions.index:
            cur = (offer*positions['position.size'][epic]) / total_funds_95
            size = positions['position.size'][epic]
            print(epic, positions['position.size'][epic])
        else:
            cur = 0
            size = 0
        if new - cur > 0.05:
            order = {'epic': epic, 'size': round((new-cur)*total_funds_95/offer, 2), 'type': 'BUY', 'priority': abs(new)<abs(cur)}
            if abs(size + order['size']) < 1:
                order['size'] = round(order['size'])
            if order['size'] != 0:
                orders.append(order)

        elif cur - new > 0.05:
            order = {'epic': epic, 'size': round((cur-new)*total_funds_95/bid, 2), 'type': 'SELL', 'priority': abs(new)<abs(cur)}
            if abs(size - order['size']) < 1:
                order['size'] = round(order['size'])
            if order['size'] != 0:
                orders.append(order)
    
    client.logout()
    return orders