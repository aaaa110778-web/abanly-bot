import re
from flask import Flask, request
import telegram
import pandas as pd
import numpy as np
import yfinance as yf
import yahoo_fin.stock_info as si
from trade_logger.logger import log_trade, update_trade_result

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN")
bot = telegram.Bot(token=TOKEN)

@app.route('/')
def index():
    return 'Digital Analysis Bot is running.'

@app.route(f'/{TOKEN}', methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    text = update.message.text.strip().upper()
    print(f"Received: {text}")

    if text == "/START":
        bot.sendMessage(chat_id=chat_id, text="مرحباً بك في بوت التحليل الرقمي للأسهم!", reply_to_message_id=msg_id)
        return 'ok'

    try:
        symbol = re.sub(r'\W+', '', text)
        stock_data = yf.Ticker(symbol).history(period='6mo')

        if stock_data.empty:
            bot.sendMessage(chat_id=chat_id, text="❌ لم يتم العثور على بيانات للسهم.", reply_to_message_id=msg_id)
            return 'ok'

        close = stock_data['Close']
        trend = np.polyfit(range(len(close)), close.values, 1)[0]
        average_volume = stock_data['Volume'].mean()
        last_price = close.iloc[-1]

        # أهداف عشوائية مبنية على الترند
        target1 = round(last_price * 1.03, 2)
        target2 = round(last_price * 1.06, 2)
        target3 = round(last_price * 1.10, 2)
        stop_loss = round(last_price * 0.94, 2)
        rating = "✅ ممتاز" if trend > 0 else "❌ ضعيف"
        score = round((trend / last_price) * 100, 2)

        # إرسال النتيجة
        analysis = f"""
📊 تحليل رقمي لسهم {symbol}

🔹 السعر الحالي: {last_price:.2f}
🎯 الأهداف: 
 - الهدف 1: {target1}
 - الهدف 2: {target2}
 - الهدف 3: {target3}
🛑 وقف الخسارة: {stop_loss}
📈 الاتجاه: {"صاعد 📈" if trend > 0 else "هابط 📉"}
📊 التقييم: {rating}
📍 نسبة تقييم الصفقة: {score}%
        """
        bot.sendMessage(chat_id=chat_id, text=analysis, reply_to_message_id=msg_id)

        # تسجيل الصفقة في سجل التعلم الذاتي
        log_trade(symbol=symbol, strategy="digital", entry_price=last_price, targets=[target1, target2, target3], stop_loss=stop_loss, score=score)

    except Exception as e:
        bot.sendMessage(chat_id=chat_id, text=f"حدث خطأ أثناء التحليل: {e}", reply_to_message_id=msg_id)

    return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    webhook_url = f"https://<YOUR APP NAME>.onrender.com/{TOKEN}"
    s = bot.setWebhook(webhook_url)
    return "webhook setup ok" if s else "webhook setup failed"

if __name__ == '__main__':
    app.run(debug=True)
