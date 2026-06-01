import requests

BOT_TOKEN = "8316233634:AAGHkYtIvWtyBRRxG9UeOcJ4FzjZvQdNrFI"
CHAT_ID = "5311676923"

url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

r = requests.post(
    url,
    data={
        "chat_id": CHAT_ID,
        "text": "Test message from Python"
    }
)

print(r.status_code)
print(r.text)