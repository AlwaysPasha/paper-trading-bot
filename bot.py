import yfinance as yf
import pandas as pd
from datetime import datetime

STARTING_CASH = 100000

stocks = ["TCS.NS", "INFY.NS", "RELIANCE.NS"]

portfolio_file = "portfolio.csv"
history_file = "trade_history.csv"

try:
    portfolio = pd.read_csv(portfolio_file)
except:
    portfolio = pd.DataFrame(columns=["stock", "shares", "buy_price"])

try:
    history = pd.read_csv(history_file)
except:
    history = pd.DataFrame(columns=["timestamp","stock","action","price","shares"])

for symbol in stocks:

    data = yf.Ticker(symbol).history(period="3mo")

    data["MA5"] = data["Close"].rolling(5).mean()
    data["MA20"] = data["Close"].rolling(20).mean()

    latest = data.iloc[-1]

    price = round(latest["Close"], 2)

    signal = "BUY" if latest["MA5"] > latest["MA20"] else "SELL"

    holding = portfolio[portfolio["stock"] == symbol]

    if signal == "BUY" and holding.empty:

        portfolio.loc[len(portfolio)] = [symbol, 1, price]

        history.loc[len(history)] = [
            datetime.now(),
            symbol,
            "BUY",
            price,
            1
        ]

        print(f"BUY {symbol} @ ₹{price}")

    elif signal == "SELL" and not holding.empty:

        history.loc[len(history)] = [
            datetime.now(),
            symbol,
            "SELL",
            price,
            int(holding.iloc[0]["shares"])
        ]

        portfolio = portfolio[portfolio["stock"] != symbol]

        print(f"SELL {symbol} @ ₹{price}")

portfolio.to_csv(portfolio_file, index=False)
history.to_csv(history_file, index=False)

print("\nCurrent Portfolio")
print(portfolio)
