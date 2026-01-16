from confluent_kafka import Consumer, KafkaError
import json
from config.config import KAFKA_BOOTSTRAP, KAFKA_TOPIC, API_KEY, API_SECRET, QUANTITY, SYMBOL, COIN, logger
from account_manager import AccountManager
from trading.strategies.rsi_strategy import RSIStrategy






account = AccountManager(API_KEY, API_SECRET, testnet=True)
strategy = RSIStrategy()


# Consumer config
consumer_conf = {
    'bootstrap.servers': KAFKA_BOOTSTRAP,
    'group.id': 'trading-bot-group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': True,
}
consumer = Consumer(consumer_conf)
consumer.subscribe([KAFKA_TOPIC])


def delivery_report(err, msg):
    if err is not None:
        print(f'Signal delivery failed: {err}')
    else:
        print(f'Signal delivered to {msg.topic()} [{msg.partition()}]')

print("Trading Bot started... Waiting for candles from Kafka")


try:
    while True:
        msg = consumer.poll(timeout=1.0)
        print("Polling Kafka... (timeout 1s)")
        if msg is None:
            print("No new message yet, waiting...")
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(f"Consumer error: {msg.error()}")
                break

        try:
            data = json.loads(msg.value().decode('utf-8'))
            close_price  = data['close']
            interval = data['interval']
            print(f"New candle {interval} | Close = {close_price}")

            action = strategy.signal_trade(close_price)
            print(f"price_history:{strategy.price_history}")
            print(f"RSI:{strategy.calculate_rsi()}")
            if action == 'BUY':
                account.create_order('BUY', QUANTITY)
                logger.info(
                f"TRADE | BUY | price={close_price} | qty={QUANTITY} | "
                f"rsi={strategy.calculate_rsi():.2f} | interval={interval} |"
                f"usdt={account.get_balance("USDT"):.2f}"
                )
            elif action == 'SELL':
                if account.can_sell(QUANTITY):
                    account.create_order('SELL', QUANTITY)
                    logger.info(
                    f"TRADE | SELL | price={close_price} | qty={QUANTITY} | "
                    f"rsi={strategy.calculate_rsi():.2f} | interval={interval} | "
                    f"usdt={account.get_balance("USDT"):.2f}"
                    )
                else:
                    logger.warning("Not enough balance to sell")
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON: {e}")
        except Exception as e:
            logger.error(f"Processing error: {e}")
        except Exception as e:
            print(f"Error processing message: {e}")

except KeyboardInterrupt:
    print("Stopping trading bot...")

finally:
    consumer.close()
    print("Trading bot stopped.")