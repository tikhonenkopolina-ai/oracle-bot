
import json
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

PRED_FILE = "predictions.json"

def load(path, default):
    try:
        with open(path, "r", encoding="utf8") as f:
            return json.load(f)
    except:
        return default

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ну привет. Я даю предсказания только по запросу, бесплатно и без расписаний 🤡✨")

async def future(update: Update, context: ContextTypes.DEFAULT_TYPE):
    preds = load(PRED_FILE, [])
    if not preds:
        await update.message.reply_text("Предсказаний нет, жизнь сурова.")
        return
    import random
    chosen = random.choice(preds)
    await update.message.reply_text(chosen["text"])

def main():
    app = ApplicationBuilder().token("PUT_YOUR_TOKEN_HERE").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("future", future))
    app.run_polling()

if __name__ == "__main__":
    main()
