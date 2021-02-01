import pandas as pd


def calculate_funds(portfolio: pd.DataFrame, cash: float) -> float:
    funds = cash
    for index, row in portfolio.iterrows():
        funds += row['position.size']*row['Open']
    return funds