import os
import logging

KAFKA_BOOTSTRAP= "your_kafka_bootstrap_server"
KAFKA_TOPIC = "your_kafka_topic"

WS_URL = "wss://stream.binance.com:9443/ws/btcusdt@kline_1m"
API_KEY = 'your_api_key_here'
API_SECRET = 'your_secret_here'

# Replace it with your preferred trading pair.
COIN = 'BTC'
SYMBOL = 'BTCUSDT'
QUANTITY = 0.001
RSI_PERIOD = 14
RSI_OVERBOUGHT = 80
RSI_OVERSOLD = 20



LOG_FILE = os.path.abspath("trades.log")

logger = logging.getLogger("trading_bot")
logger.setLevel(logging.INFO)

# Avoid adding handlers multiple times during reload
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