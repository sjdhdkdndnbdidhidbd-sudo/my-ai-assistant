from flask import Flask, request
import google.generativeai as genai
import os
import requests

app = Flask(__name__)

# Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

# Telegram
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

@app.route("/")
def home():
    return "Telegram AI Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if not data:
        return "No data", 400

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        user_text = data["message"].get("text", "")

        # /start কমান্ড
        if user_text == "/start":
            reply = (
                "👋 আসসালামু আলাইকুম!\n\n"
                "আমি তোমার AI Assistant।\n"
                "যেকোনো প্রশ্ন করো, আমি উত্তর দেওয়ার চেষ্টা করব।"
            )
        else:
            try:
                response = model.generate_content(user_text)
                reply = response.text
            except Exception as e:
                reply = f"❌ Error:\n{str(e)}"

        requests.post(
            f"{TELEGRAM_API}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": reply
            }
        )

    return "OK", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", ...)))
