import logging
import openai
import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from saudi_price_scraper import get_saudi_price
from yakeen_scraper import check_sharia
from news_fetcher import fetch_news

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
DAILY_PASSWORD = "123123"
AUTHORIZED_USERS = {}

openai.api_key = OPENAI_API_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔒 أرسل كلمة السر للمتابعة.")

async def handle_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if AUTHORIZED_USERS.get(user_id):
        return
    if update.message.text == DAILY_PASSWORD:
        AUTHORIZED_USERS[user_id] = True
        await update.message.reply_text("✅ تم التحقق. أرسل اسم السهم الآن.")
    else:
        await update.message.reply_text("❌ كلمة السر غير صحيحة.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if not AUTHORIZED_USERS.get(user_id, False):
        await update.message.reply_text("🔒 أرسل كلمة السر أولاً.")
        return

    symbol = update.message.text.strip().upper()
    saudi = not symbol.isascii()
    price = get_saudi_price(symbol) if saudi else get_us_price(symbol)

    if not price:
        await update.message.reply_text("❌ لم يتم العثور على السعر.")
        return

    sharia = check_sharia(symbol) if saudi else "✅ شرعي (تحليل خارجي)"
    news = fetch_news(symbol)

    try:
        gpt_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "أنت محلل فني محترف. استخدم السعر والشرعية والأخبار لتوليد توصية احترافية."},
                {"role": "user", "content": f"حلل سهم {symbol}، السعر الحالي {price}، الشرعية: {sharia}، الأخبار: {news}"}
            ]
        )
        reply = gpt_response["choices"][0]["message"]["content"]
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text(f"❌ خطأ أثناء التحليل: {e}")

def get_us_price(symbol):
    url = f"https://api.polygon.io/v2/last/trade/stocks/{symbol}?apiKey={POLYGON_API_KEY}"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        return data.get("results", {}).get("p")
    return None

def main():
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_password))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
