from binance.client import Client
import pandas as pd

from indicators import add_indicators, is_golden_cross, is_strong_signal
from telegram import send_message

client = Client()

golden = []
strong = []


def get_symbols():
    info = client.get_exchange_info()

    symbols = []

    for s in info["symbols"]:
        if (
            s["quoteAsset"] == "USDT"
            and s["status"] == "TRADING"
            and s["isSpotTradingAllowed"]
        ):
            symbols.append(s["symbol"])

    return symbols


def get_dataframe(symbol):

    klines = client.get_klines(
        symbol=symbol,
        interval=Client.KLINE_INTERVAL_1DAY,
        limit=250,
    )

    df = pd.DataFrame(
        klines,
        columns=[
            "time",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "close_time",
            "qav",
            "trades",
            "tbav",
            "tqav",
            "ignore",
        ],
    )

    df["close"] = df["close"].astype(float)
    df["volume"] = df["volume"].astype(float)

    return add_indicators(df)


for symbol in get_symbols():

    try:

        df = get_dataframe(symbol)

        if is_golden_cross(df):
            golden.append(symbol)

        if is_strong_signal(df):
            strong.append(symbol)

        print(symbol)

    except Exception as e:
        print(symbol, e)


message1 = "📈 <b>Golden Cross امروز</b>\n\n"

if len(golden) == 0:
    message1 += "❌ هیچ Golden Cross جدیدی پیدا نشد."
else:
    for s in golden:
        message1 += f"✅ {s}\n"

send_message(message1)


message2 = "⭐ <b>سیگنال‌های منتخب</b>\n\n"

if len(strong) == 0:
    message2 += "❌ هیچ سیگنال قدرتمندی پیدا نشد."
else:
    for s in strong:
        message2 += f"🚀 {s}\n"

send_message(message2)
