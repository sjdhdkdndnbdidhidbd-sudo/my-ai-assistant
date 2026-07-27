from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

@app.route("/")
def home():
    return "My AI Assistant is running!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    prompt = data.get("message", "")

    response = model.generate_content(prompt)

    return jsonify({
        "reply": response.text
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
