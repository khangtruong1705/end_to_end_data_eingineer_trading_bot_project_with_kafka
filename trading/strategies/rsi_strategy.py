import talib
import numpy as np
import logging
from config.config import RSI_PERIOD, RSI_OVERBOUGHT, RSI_OVERSOLD

class RSIStrategy:
    def __init__(self):
        self.price_history = []  

    def add_price(self, price):
        self.price_history.append(price)
        if len(self.price_history) > RSI_PERIOD + 1:  
            self.price_history.pop(0)

    def calculate_rsi(self):
        if len(self.price_history) < RSI_PERIOD + 1:
            return None
        np_prices = np.array(self.price_history)
        rsi = talib.RSI(np_prices, timeperiod=RSI_PERIOD)[-1]
        return rsi

    def signal_trade(self, current_price):
        self.add_price(current_price)
        rsi = self.calculate_rsi()
        if rsi is None:
            return None

        logging.info(f"RSI: {rsi}")
        if rsi > RSI_OVERBOUGHT:
            return 'SELL'
        elif rsi < RSI_OVERSOLD:
            return 'BUY'
        return None 