import yfinance as yf
import pandas as pd
from datetime import datetime
import requests

stocks = ["TCS.NS", "INFY.NS", "RELIANCE.NS"]

portfolio_file = "portfolio.csv"
history_file = "trade_history.csv"
cash_file = "cash.txt"

BOT_TOKEN = "8316233634:AAGHkYtIvWtyBRRxG9UeOcJ4FzjZvQdNrFI
CHAT_ID = "5311676923"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
        )

with open(cash_file, "r") as f:
    cash = float(f.read().strip())

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

    if signal == "BUY" and holding.empty and cash >= price:

        portfolio.loc[len(portfolio)] = [symbol, 1, price]

        cash -= price

        history.loc[len(history)] = [
            datetime.now(),
            symbol,
            "BUY",
            price,
            1
        ]

        print(f"BUY {symbol} @ ₹{price}")
        send_telegram(
            f"🔴 SELL {symbol}\nPrice: ₹{price}\nCash Balance: ₹{cash:.2f}"
        )

        send_telegram(
            f"🚀 BUY {symbol}\nPrice: ₹{price}\nCash Balance: ₹{cash:.2f}"
        )

    elif signal == "SELL" and not holding.empty:

        cash += price * int(holding.iloc[0]["shares"])

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

with open(cash_file, "w") as f:
    f.write(str(round(cash, 2)))

holdings_value = 0

for _, row in portfolio.iterrows():
    try:
        current_price = yf.Ticker(row["stock"]).history(period="1d")["Close"].iloc[-1]
        holdings_value += current_price * row["shares"]
    except:
        pass

total_value = cash + holdings_value
profit_loss = total_value - 100000

print(f"\nCash Balance: ₹{cash:.2f}")
print(f"Holdings Value: ₹{holdings_value:.2f}")
print(f"Total Portfolio Value: ₹{total_value:.2f}")
print(f"Profit/Loss: ₹{profit_loss:.2f}")

print("\nCurrent Portfolio")
print(portfolio)