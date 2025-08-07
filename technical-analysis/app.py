from flask import Flask, request
import telegram
import os
import re
import yfinance as yf
from ta.momentum import RSIIndicator
from ta.trend import MACD
from ta.volatility import BollingerBands
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from trade_logger import log_trade, update_trade_result

TOKEN = os.getenv("BOT_TOKEN")
bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)
images_path = "./images"

if not os.path.exists(images_path):
    os.mkdir(images_path)

@app.route('/')
def index():
    return 'Technical Analysis Bot is running.'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook(f'https://<YOUR APP>.onrender.com/{TOKEN}')
    return "webhook setup ok" if s else "webhook setup failed"

@app.route(f'/{TOKEN}', methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    text = update.message.text.encode('utf-8').decode()

    if text == "/start":
        welcome = "🤖 مرحباً بك في بوت التحليل الفني للأسهم.\nأرسل رمز السهم (مثل: AAPL أو TSLA)."
        bot.sendMessage(chat_id=chat_id, text=welcome, reply_to_message_id=msg_id)
        return 'ok'

    try:
        symbol = re.sub(r"\W", "", text.upper())
        df = yf.download(symbol, period="6mo")
        close = df["Close"]

        # التحليل
        macd = MACD(close).macd_diff()
        rsi = RSIIndicator(close).rsi()
        bb = BollingerBands(close)
        upper_band = bb.bollinger_hband()
        lower_band = bb.bollinger_lband()

        current_price = close.iloc[-1]
        signal = ""
        rating = 50

        if macd.iloc[-1] > 0:
            signal += "✅ MACD إيجابي\n"
            rating += 10
        else:
            signal += "❌ MACD سلبي\n"
            rating -= 10

        if rsi.iloc[-1] < 30:
            signal += "✅ RSI في منطقة شراء\n"
            rating += 10
        elif rsi.iloc[-1] > 70:
            signal += "❌ RSI في منطقة بيع\n"
            rating -= 10

        if current_price < lower_band.iloc[-1]:
            signal += "✅ السعر تحت البولنجر السفلي\n"
            rating += 10
        elif current_price > upper_band.iloc[-1]:
            signal += "❌ السعر فوق البولنجر العلوي\n"
            rating -= 10

        # الأهداف ووقف الخسارة
        stop_loss = round(current_price * 0.95, 2)
        target1 = round(current_price * 1.03, 2)
        target2 = round(current_price * 1.06, 2)
        target3 = round(current_price * 1.09, 2)

        log_trade(symbol, current_price, [target1, target2, target3], stop_loss, "technical", rating)

        bot.sendMessage(
            chat_id=chat_id,
            text=f"""
📉 السهم: {symbol}
💵 السعر الحالي: {current_price:.2f}$
🎯 الأهداف: {target1}$ - {target2}$ - {target3}$
🛡️ وقف الخسارة: {stop_loss}$
📊 التقييم: {rating}%
📥 التوصية: {"شراء" if rating >= 60 else "انتظار"}
---
{signal}
""".strip()
        )

        update_trade_result(symbol, current_price)

    except Exception as e:
        bot.sendMessage(chat_id=chat_id, text="⚠️ حدث خطأ في التحليل. تأكد من كتابة الرمز بشكل صحيح.")

    return 'ok'
