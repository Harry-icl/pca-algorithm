def execute_trades(orders, portfolio, cash) -> "pd.DataFrame":
    fees = 0
    for order in orders:
        if order['type'] == "BUY":
            init_cash = cash
            if portfolio['position.size'][order['epic']] < 0 and portfolio['position.size'][order['epic']] + order['size'] > 0:
                cash += portfolio['position.size'][order['epic']]*portfolio['Open'][order['epic']]*(1+fees)
                cash -= (order['size'] + portfolio['position.size'][order['epic']])*portfolio['Open'][order['epic']]*(1+fees)
            elif portfolio['position.size'][order['epic']] < 0:
                cash -= order['size']*portfolio['Open'][order['epic']]*(1+fees)
            else:
                cash -= order['size']*portfolio['Open'][order['epic']]*(1+fees)
            portfolio['position.size'][order['epic']] += order['size']
            cash_change = cash - init_cash
            print("%s units of %s bought @ %s, cash change: %s" % (order['size'], order['epic'], portfolio['Open'][order['epic']], cash_change))
        
        elif order['type'] == "SELL":
            init_cash = cash
            if portfolio['position.size'][order['epic']] > 0 and portfolio['position.size'][order['epic']] - order['size'] < 0:
                cash += portfolio['position.size'][order['epic']]*portfolio['Open'][order['epic']]*(1-fees)
                cash += (order['size'] - portfolio['position.size'][order['epic']])*portfolio['Open'][order['epic']]*(1-fees)
            elif portfolio['position.size'][order['epic']] > 0:
                cash += order['size']*portfolio['Open'][order['epic']]*(1-fees)
            else:
                cash += order['size']*portfolio['Open'][order['epic']]*(1-fees)
            portfolio['position.size'][order['epic']] -= order['size']
            cash_change = cash - init_cash
            print("%s units of %s sold @ %s, cash change: %s" % (order['size'], order['epic'], portfolio['Open'][order['epic']], cash_change))
    return portfolio, cash