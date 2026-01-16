import websocket
import json
import time
from confluent_kafka import Producer
from config.config import KAFKA_BOOTSTRAP, KAFKA_TOPIC, WS_URL,SYMBOL


conf = {
    'bootstrap.servers': KAFKA_BOOTSTRAP,
    'client.id': 'binance-stream-producer',
    'acks': 'all',
    'retries': 3,
}

producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print(f'Delivery failed: {err}')
    else:
        print(f'Delivered to {msg.topic()} [{msg.partition()}] @ offset {msg.offset()}')



def on_message(ws, message):
    try:
        data = json.loads(message)
        kline = data['k']
        if not kline['x']:
            return
        close_price = float(kline['c'])
        open_price = float(kline['o'])
        high_price = float(kline['h'])
        low_price = float(kline['l'])
        volume = float(kline['v'])
        close_time = kline['T'] / 1000.0

        enhanced_data = {
            'symbol': kline['s'],
            'interval': kline['i'],
            'open': open_price,
            'high': high_price,
            'low': low_price,
            'close': close_price,
            'volume': volume,
            'timestamp': close_time
        }

        producer.produce(
            topic=KAFKA_TOPIC,
            value=json.dumps(enhanced_data).encode("utf-8"),
            key=kline['s'].encode("utf-8"),
            on_delivery=delivery_report
        )
        producer.poll(0)

        print(
            f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] "
            f"Chart {SYMBOL} close klin {kline['i']} | Close: {close_price}"
        )

    except Exception as e:
        print(f"Error processing message: {e}")

def on_error(ws, error):
    print(f"WebSocket Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print(f"WebSocket Closed: {close_status_code} - {close_msg}")
    producer.flush()
    print("Retrying connection in 5 seconds...")
    time.sleep(5)
    run_websocket()  # Reconnect tự động

def on_open(ws):
    print("Successfully connected to Binance WebSocket!")
    print("Sending real-time prices to Kafka...")

def run_websocket():
    ws = websocket.WebSocketApp(
        WS_URL,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever(
        ping_interval=30,
        ping_timeout=10,
        reconnect=True  
    )

if __name__ == "__main__":
    print("Starting Kafka producer + Binance stream...")
    run_websocket()
    producer.flush()