import telebot
import os
from datetime import datetime
from utils.analysis import analyze_stock
from utils.auth import is_authenticated, save_access
from utils.news import get_stock_news
from utils.shariah import check_shariah_status

API_KEY = os.getenv("TELEGRAM_API_KEY", "7250935830:AAEhcPifdrDk9Bxufd-rpsm2nM-cehkSAuk")
bot = telebot.TeleBot(API_KEY)

PASSWORD = "123123"
authenticated_users = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    today = datetime.now().strftime("%Y-%m-%d")
    if not is_authenticated(user_id, today):
        bot.reply_to(message, "أدخل كلمة السر للاستخدام:")
        save_access(user_id, today, False)
    else:
        bot.reply_to(message, "مرحباً بك! أرسل اسم السهم.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    today = datetime.now().strftime("%Y-%m-%d")
    auth = is_authenticated(user_id, today)

    if not auth:
        if message.text.strip() == PASSWORD:
            save_access(user_id, today, True)
            bot.reply_to(message, "تم التحقق. الآن أرسل اسم السهم.")
        else:
            bot.reply_to(message, "كلمة السر غير صحيحة.")
        return

    stock_symbol = message.text.strip().upper()
    bot.reply_to(message, f"جاري تحليل السهم {stock_symbol} ...")

    try:
        result = analyze_stock(stock_symbol)
        news = get_stock_news(stock_symbol)
        shariah = check_shariah_status(stock_symbol)

        msg = f"📊 تحليل السهم: {stock_symbol}

"
        msg += result + "

"
        if news:
            msg += f"📰 خبر مؤثر: {news}

"
        msg += f"📜 الشرعية: {shariah}"
        bot.reply_to(message, msg)
    except Exception as e:
        bot.reply_to(message, f"حدث خطأ أثناء تحليل السهم: {str(e)}")

bot.polling()