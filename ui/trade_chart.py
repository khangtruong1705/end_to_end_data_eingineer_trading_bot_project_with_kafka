import asciichartpy as ac
import time
import os
import re

LOG_FILE = os.path.abspath("trades.log")

price_pattern = re.compile(r"price=([\d.]+)")

def read_prices():
    prices = []
    if not os.path.exists(LOG_FILE):
        return prices

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            match = price_pattern.search(line)
            if match:
                prices.append(float(match.group(1)))
    return prices


def draw_chart(prices):
    if len(prices) < 2:
        print("Not enough data to draw chart")
        return

    config = {
        "height": 15,
        "format": "{:,.2f}"
    }

    print("\033c", end="")
    print("📈 TRADE PRICE CHART (BUY/SELL)")
    print(ac.plot(prices[-50:], config))


if __name__ == "__main__":
    while True:
        prices = read_prices()
        draw_chart(prices)
        time.sleep(2)
