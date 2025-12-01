
import json
import random
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

PRED_FILE = "predictions.json"
USER_FILE = "users.json"
STATE_FILE = "day_state.json"  # tracks used predictions per day


def load_json(path, default):
    try:
        with open(path, "r", encoding="utf8") as f:
            return json.load(f)
    except:
        return default


def save_json(path, data):
    with open(path, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users = load_json(USER_FILE, {})
    uid = str(update.effective_user.id)

    if uid not in users:
        users[uid] = {"subscribed": True}
        save_json(USER_FILE, users)

    await update.message.reply_text(
        "Ты подписан на мои ежедневные предсказания. "
        "31 день боли, иронии и лёгкого оскорбления. Начинаем 15 декабря 🤡✨"
    )


async def future(update: Update, context: ContextTypes.DEFAULT_TYPE):
    today = datetime.now().date()
    start_date = datetime(2024, 12, 15).date()

    if today < start_date:
        await update.message.reply_text("Подожди до 15 декабря. Я ещё разгоняюсь 💅")
        return

    await send_prediction(update.effective_user.id, update)


async def send_prediction(uid, update_or_context):
    preds = load_json(PRED_FILE, [])
    state = load_json(STATE_FILE, {})  # { "YYYY-MM-DD": [used_ids...] }

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

    text = chosen["text"]

    if hasattr(update_or_context, "message"):
        await update_or_context.message.reply_text(text)
    else:
        await update_or_context.bot.send_message(chat_id=uid, text=text)


def main():
    app = ApplicationBuilder().token("PUT_YOUR_TOKEN_HERE").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("future", future))
    app.run_polling()


if __name__ == "__main__":
    main()
