import os
from flask import Flask, request
import requests

app = Flask(__name__)

# توکن ربات از متغیرهای محیطی Render خوانده می‌شود
TOKEN = os.environ.get("BALE_TOKEN")
BASE_URL = f"https://tapi.bale.ai/bot{TOKEN}"

# آدرس سایت شما در گیت‌هاب پیجز
GITHUB_PAGE_URL = "https://wwwjangisadegh96-png.github.io/my-booking-bot/"

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!"

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if data and "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        
        # اگر کاربر دستور /start را فرستاد
        if text == "/start":
            send_welcome_message(chat_id)
            
    return {"status": "ok"}

def send_welcome_message(chat_id):
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": "سلام! 👋\nبرای ورود به سایت، روی دکمه زیر کلیک کنید:",
        "reply_markup": {
            "inline_keyboard": [
                [
                    {
                        "text": "🌐 ورود به سایت",
                        "url": GITHUB_PAGE_URL
                    }
                ]
            ]
        }
    }
    requests.post(url, json=payload)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)