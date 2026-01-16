import asciichartpy as ac
import time
import os
import re

LOG_FILE = os.path.abspath("trades.log")

usdt_pattern = re.compile(r"usdt=([\d.]+)")

def read_usdt_values():
    usdt_values = []
    if not os.path.exists(LOG_FILE):
        return usdt_values

    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            match = usdt_pattern.search(line)
            if match:
                usdt_values.append(float(match.group(1)))
    return usdt_values


def draw_chart(usdt_values):
    if len(usdt_values) < 2:
        print("Not enough data to draw chart")
        return

    config = {
        "height": 15,
        "format": "{:,.2f}"
    }

    print("\033c", end="")
    print("💰 USDT BALANCE CHART")
    print(ac.plot(usdt_values[-50:], config))


if __name__ == "__main__":
    while True:
        usdt_values = read_usdt_values()
        draw_chart(usdt_values)
        time.sleep(30)
