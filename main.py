
import logging
import yfinance as yf
from telegram import Update, Bot
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, CallbackContext
import pandas as pd
import datetime

# إعدادات البوت
TOKEN = "7250935830:AAEhcPifdrDk9Bxufd-rpsm2nM-cehkSAuk"
PASSWORD = "123123"
AUTHORIZED_USERS = set()
STOCK_MAP = {
    "الراجحي": "1120.SE",
    "أرامكو": "2222.SE",
    "سابك": "2010.SE",
    "المجموعة السعودية": "2250.SE",
    "سيرا": "1810.SE",
}

# تهيئة البوت
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("مرحبًا! أرسل كلمة السر أولًا.")

def authenticate(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    if text == PASSWORD:
        AUTHORIZED_USERS.add(user_id)
        update.message.reply_text("✅ تم التحقق! الآن أرسل اسم السهم لتحليله.")
    else:
        update.message.reply_text("❌ كلمة السر غير صحيحة.")

def get_stock_symbol(name_or_symbol: str):
    name = name_or_symbol.strip().upper()
    if name in STOCK_MAP:
        return STOCK_MAP[name]
    if name.isalpha() and len(name) <= 5:
        return name  # أمريكي غالباً
    return None

def analyze_stock(symbol: str):
    try:
        data = yf.download(symbol, period="6mo", interval="1d", progress=False)
        if data.empty:
            return "❌ لم يتم العثور على بيانات للسهم."

        high = data["High"].max()
        low = data["Low"].min()
        current_price = data["Close"].iloc[-1]
        step = (high - low) / 24
        levels = [low + i * step for i in range(25)]
        near_levels = [lvl for lvl in levels if abs(lvl - current_price) <= step * 3]

        msg = f"🔍 تحليل رقمي وفني لسهم {symbol}:
"
        msg += f"• السعر الحالي: {current_price:.2f}
"
        msg += f"• أعلى سعر: {high:.2f}
• أقل سعر: {low:.2f}
"
        msg += f"• أقرب المستويات:
" + "
".join([f"- {lvl:.2f}" for lvl in near_levels])

        if current_price > levels[-2]:
            msg += "
✅ السهم قريب من المقاومة العليا."
        elif current_price < levels[1]:
            msg += "
⚠️ السهم قريب من الدعم السفلي."

        return msg

    except Exception as e:
        return f"حدث خطأ أثناء التحليل: {str(e)}"

def handle_message(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id not in AUTHORIZED_USERS:
        update.message.reply_text("🚫 أرسل كلمة السر أولًا.")
        return

    text = update.message.text.strip()
    symbol = get_stock_symbol(text)
    if not symbol:
        update.message.reply_text("❌ لم يتم التعرف على السهم.")
        return

    msg = analyze_stock(symbol)
    update.message.reply_text(msg)

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, authenticate))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
