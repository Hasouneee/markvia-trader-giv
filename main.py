
import os
import requests
from flask import Flask

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL = os.getenv("TELEGRAM_CHANNEL", "@YOUR_CHANNEL")

@app.route("/")
def home():
    return "MARKVIA TRADER GIV Bot is running!"

@app.route("/health")
def health():
    return "OK", 200

@app.route("/send")
def send_message():
    if not TOKEN:
        return "Missing bot token", 500

    text = "🚀 MARKVIA TRADER GIV\n\nالبوت يعمل بنجاح!"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    response = requests.post(url, json={
        "chat_id": CHANNEL,
        "text": text
    }, timeout=15)

    return response.text, response.status_code

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))
  
