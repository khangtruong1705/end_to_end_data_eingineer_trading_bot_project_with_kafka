import os
import logging

KAFKA_BOOTSTRAP= "localhost:9092"
KAFKA_TOPIC = "crypto_prices"

WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"
API_KEY = 'Kml1sR7NRMMBhH9LsC9EAHe7WFmlsVzxVfUzmBklBJrJJEuRj625yzQeResvdwa6'
API_SECRET = 'BaXiq2WV2LXML1kmMmLiXknaOiY1OvItEj7PeFMM5M7wW5JYX50FJlc81QaMr5Ai'

COIN = 'BTC'
SYMBOL = 'BTCUSDT'
QUANTITY = 0.001  
RSI_PERIOD = 14
RSI_OVERBOUGHT = 80
RSI_OVERSOLD = 20



LOG_FILE = os.path.abspath("trades.log")

logger = logging.getLogger("trading_bot")
logger.setLevel(logging.INFO)


if not logger.handlers:
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    stream_handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)