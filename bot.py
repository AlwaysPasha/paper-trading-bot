import yfinance as yf
import pandas as pd
from datetime import datetime
import os

stocks = ["TCS.NS", "INFY.NS", "RELIANCE.NS"]

trades = []

for symbol in stocks:
    data = yf.Ticker(symbol).history(period="3mo")

    data["MA5"] = data["Close"].rolling(5).mean()
    data["MA20"] = data["Close"].rolling(20).mean()

    latest = data.iloc[-1]

    signal = "BUY" if latest["MA5"] > latest["MA20"] else "SELL"

    trades.append({
        "timestamp": datetime.now(),
        "stock": symbol,
        "price": round(latest["Close"], 2),
        "MA5": round(latest["MA5"], 2),
        "MA20": round(latest["MA20"], 2),
        "signal": signal
    })

df = pd.DataFrame(trades)

print(df)

file_name = "paper_trades.csv"

if os.path.exists(file_name):
    df.to_csv(file_name, mode="a", header=False, index=False)
else:
    df.to_csv(file_name, index=False)