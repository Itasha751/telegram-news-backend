from flask import Flask, jsonify
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from dotenv import load_dotenv
import os, pytz
from datetime import datetime

load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")

app = Flask(__name__)

@app.route("/posts", methods=["GET"])
def get_posts():
    channel_url = "https://t.me/RTarabic"  # תחליף או תאפשר בחירה בעתיד
    posts_data = []
    israel_tz = pytz.timezone("Asia/Jerusalem")

    with TelegramClient("session", api_id, api_hash) as client:
        channel = client.get_entity(channel_url)
        history = client(GetHistoryRequest(
            peer=channel,
            limit=10,
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0
        ))

        for message in history.messages:
            if not message.message:
                continue

            dt = message.date.astimezone(israel_tz)
            posts_data.append({
                "text": message.message,
                "date": dt.strftime("%Y-%m-%d %H:%M"),
                "media": None  # נוסיף בהמשך
            })

    return jsonify(posts_data)

if __name__ == "__main__":
    app.run(debug=True)
