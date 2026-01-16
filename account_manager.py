# src/account_manager.py
from binance.client import Client
from binance.exceptions import BinanceAPIException
import logging
from config.config import SYMBOL,COIN

logging.basicConfig(level=logging.INFO)

class AccountManager:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret, testnet=testnet)
        self.symbol = SYMBOL

    def get_balance(self, asset=COIN):
        try:
            balance = self.client.get_asset_balance(asset=asset)
            return float(balance['free'])
        except BinanceAPIException as e:
            logging.error(f"Error getting balance: {e}")
            return 0.0

    def create_order(self, side, quantity):
        try:
            order = self.client.create_order(
                symbol=self.symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
            print(f"{side} order executed !!")
            return order
        except BinanceAPIException as e:
            logging.error(f"Error creating order: {e}")
            return None

    def can_sell(self, quantity, asset=COIN):
        return self.get_balance(asset) >= quantity