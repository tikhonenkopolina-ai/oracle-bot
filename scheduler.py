
import json
import random
from datetime import datetime
from telegram import Bot

TOKEN = "PUT_YOUR_TOKEN_HERE"
USER_FILE = "users.json"
PRED_FILE = "predictions.json"
STATE_FILE = "day_state.json"

bot = Bot(token=TOKEN)


def load_json(path, default):
    try:
        with open(path, "r", encoding="utf8") as f:
            return json.load(f)
    except:
        return default


def save_json(path, data):
    with open(path, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def choose_prediction():
    preds = load_json(PRED_FILE, [])
    state = load_json(STATE_FILE, {})

    today_key = datetime.now().strftime("%Y-%m-%d")
    if today_key not in state:
        state[today_key] = []

    available = [p for p in preds if p["id"] not in state[today_key]]

    if not available:
        state[today_key] = []
        available = preds

    chosen = random.choice(available)
    state[today_key].append(chosen["id"])
    save_json(STATE_FILE, state)

    return chosen["text"]


def run_daily():
    users = load_json(USER_FILE, {})
    today = datetime.now().date()
    start_date = datetime(2024, 12, 15).date()

    if today < start_date:
        return

    for uid in users.keys():
        msg = choose_prediction()
        bot.send_message(chat_id=uid, text=msg)


if __name__ == "__main__":
    run_daily()
