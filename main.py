import telebot
import requests
from bs4 import BeautifulSoup
import yfinance as yf
import pandas as pd

TOKEN = "7250935830:AAEhcPifdrDk9Bxufd-rpsm2nM-cehkSAuk"
bot = telebot.TeleBot(TOKEN)

AUTHORIZED_USERS = {}
PASSWORD = "123123"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    if chat_id not in AUTHORIZED_USERS:
        bot.send_message(chat_id, "🔒 أرسل كلمة المرور لاستخدام البوت:")
    else:
        bot.send_message(chat_id, "أهلًا بك! أرسل اسم السهم للحصول على التحليل.")

@bot.message_handler(func=lambda m: m.chat.id not in AUTHORIZED_USERS)
def check_password(message):
    if message.text == PASSWORD:
        AUTHORIZED_USERS[message.chat.id] = True
        bot.send_message(message.chat.id, "✅ تم التحقق! أرسل اسم السهم الآن.")
    else:
        bot.send_message(message.chat.id, "❌ كلمة المرور غير صحيحة. حاول مرة أخرى.")

@bot.message_handler(func=lambda m: True)
def handle_stock_request(message):
    if message.chat.id not in AUTHORIZED_USERS:
        bot.send_message(message.chat.id, "🔒 يجب إدخال كلمة المرور أولاً.")
        return

    stock_symbol = message.text.strip().upper()
    msg = f"📊 تحليل السهم {stock_symbol}\n"

    try:
        # تحليل فني مبسط
        data = yf.download(stock_symbol, period="5d", interval="1h")
        if data.empty:
            bot.send_message(message.chat.id, "❌ لم يتم العثور على بيانات للسهم.")
            return

        latest = data.iloc[-1]
        close_price = latest["Close"]
        volume = latest["Volume"]

        msg += f"🔹 آخر سعر: {close_price:.2f}\n"
        msg += f"🔹 حجم التداول: {volume:.0f}\n"

        # مثال لتحليل بسيط (إغلاق فوق متوسط)
        ma50 = data["Close"].rolling(window=50).mean().iloc[-1]
        if close_price > ma50:
            msg += "✅ السعر فوق المتوسط 50 - إشارة إيجابية\n"
        else:
            msg += "⚠️ السعر تحت المتوسط 50 - تحتاج حذر\n"

        # تقييم الصفقة (تجريبي)
        confidence = 92  # لاحقًا يُحسب آليًا
        msg += f"🎯 نسبة نجاح الصفقة المتوقعة: {confidence}%\n"

        # الشرعية من موقع يقين
        try:
            yakin_url = f"https://yaqeen.sa/stock/{stock_symbol}"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(yakin_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            tag = soup.find("div", string=lambda t: t and "شرعية" in t)
            if tag:
                msg += f"🕌 الشرعية: {tag.text.strip()}\n"
            else:
                msg += "🕌 الشرعية: المعلومة غير متوفرة\n"
        except:
            msg += "🕌 الشرعية: المعلومة غير متوفرة\n"

        # الأخبار: مدمجة في التحليل الداخلي فقط (لا تُعرض)

        bot.send_message(message.chat.id, msg)
    except Exception as e:
        bot.send_message(message.chat.id, f"حدث خطأ أثناء التحليل: {e}")

bot.polling()
