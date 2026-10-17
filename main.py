import os
import time
import threading
import html
import feedparser
import requests
from flask import Flask

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL = os.getenv("TELEGRAM_CHANNEL")

FEEDS = [
    "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "https://feeds.marketwatch.com/marketwatch/topstories/",
]

sent_links = set()

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    response = requests.post(
        url,
        data={
            "chat_id": CHANNEL,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": False,
        },
        timeout=20,
    )
    response.raise_for_status()

def publish_news():
    for feed_url in FEEDS:
        try:
            feed = feedparser.parse(feed_url)

            for item in reversed(feed.entries[:10]):
                link = item.get("link", "").strip()
                title = item.get("title", "").strip()

                if not link or not title or link in sent_links:
                    continue

                message = (
                    "📰 <b>MARKVIA TRADER GIV</b>\n\n"
                    f"📊 {html.escape(title)}\n\n"
                    f"🔗 <a href=\"{html.escape(link, quote=True)}\">"
                    "اقرأ الخبر كاملاً</a>\n\n"
                    "⚠️ الأخبار للمعلومات فقط وليست توصية تداول."
                )

                send_message(message)
                sent_links.add(link)
                time.sleep(2)

        except Exception as error:
            print(f"Feed error: {error}")

def news_loop():
    while True:
        if TOKEN and CHANNEL:
            publish_news()
        else:
            print("Missing Telegram environment variables")

        time.sleep(1800)

@app.route("/")
def home():
    return "MARKVIA TRADER GIV Bot is running!"

if __name__ == "__main__":
    threading.Thread(target=news_loop, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "10000")))
