from flask import Flask, request, jsonify
from pyrogram import Client
from telegraph_utils import extract_telegraph_data

api_id = 28607488         # Replace with your Telegram API ID
api_hash = "bc94e7a874a66b95e28cfbabf8c29948"   # Replace with your Telegram API HASH
channel_username = "chicas_asiaticas_whaifus_y_mas"  # No @ symbol

client = Client("my_session", api_id=api_id, api_hash=api_hash)
app = Flask(__name__)

@app.route("/search")
def search():
    query = request.args.get("query", "").lower()
    if not query:
        return jsonify({"error": "Missing query param ?query=..."})

    results = []

    with client:
        for msg in client.search_messages(channel_username, query=query, limit=30):
            if msg.text and "telegra.ph" in msg.text:
                for word in msg.text.split():
                    if "telegra.ph" in word:
                        link = word.split("?")[0].strip()
                        if link.startswith("http"):
                            results.append(extract_telegraph_data(link))

    return jsonify(results)

@app.route("/")
def home():
    return jsonify({"message": "Telegraph Scraper API is running!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
