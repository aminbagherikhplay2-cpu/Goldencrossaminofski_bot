import requests
from config import BOT_TOKEN, CHAT_ID

def send_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }

    r = requests.post(url, data=data)

    return r.status_code == 200
