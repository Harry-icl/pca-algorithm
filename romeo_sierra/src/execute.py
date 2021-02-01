from .rest_client import RestClient
from .constants import *

def execute_trades(orders: list) -> None:
    client = RestClient(rest_api_key, rest_identifier, rest_password, rest_url)
    client.login()
    for order in orders:
        if order['priority']:
            dealRef = client.execute_trade(order['epic'], order['size'], order['type'])['dealReference']
            print('Processing order ' + dealRef)
            for i in range(5):
                print('.')
                success, response = client.confirm_trade(dealRef)
                if success:
                    print('Trade executed')
                    break
                else:
                    print(response)
            
    for order in orders:
        if not order['priority']:
            dealRef = client.execute_trade(order['epic'], order['size'], order['type'])['dealReference']
            print('Processing order ' + dealRef)
            for i in range(5):
                print('.')
                success, response = client.confirm_trade(dealRef)
                if success:
                    print('Trade executed')
                    break
                else:
                    print(response)

    client.logout()