import pandas as pd
import ta


def add_indicators(df):
    df["EMA50"] = ta.trend.ema_indicator(df["close"], window=50)
    df["EMA200"] = ta.trend.ema_indicator(df["close"], window=200)

    df["RSI"] = ta.momentum.rsi(df["close"], window=14)

    macd = ta.trend.MACD(df["close"])

    df["MACD"] = macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()

    df["AVG_VOLUME"] = df["volume"].rolling(20).mean()

    return df


def is_golden_cross(df):
    if len(df) < 201:
        return False

    prev = df.iloc[-2]
    last = df.iloc[-1]

    return (
        prev["EMA50"] <= prev["EMA200"]
        and last["EMA50"] > last["EMA200"]
    )


def is_strong_signal(df):
    last = df.iloc[-1]

    if not is_golden_cross(df):
        return False

    if last["RSI"] < 55 or last["RSI"] > 70:
        return False

    if last["MACD"] <= last["MACD_SIGNAL"]:
        return False

    if last["volume"] < last["AVG_VOLUME"] * 1.5:
        return False

    return True
