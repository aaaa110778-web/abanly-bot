from flask import Flask, request
import telegram
import os
import yahoo_fin.stock_info as si
from trade_logger.logger import log_trade, update_trade_result

app = Flask(__name__)
TOKEN = os.environ.get("BOT_TOKEN")
bot = telegram.Bot(token=TOKEN)

@app.route('/')
def index():
    return 'Dividend Bot is running.'

@app.route(f"/{TOKEN}", methods=["POST"])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    text = update.message.text.strip().upper()

    if text == "/START":
        bot.sendMessage(chat_id=chat_id, text="مرحباً بك في بوت توزيعات الأرباح!", reply_to_message_id=msg_id)
        return "ok"

    try:
        df = si.get_dividends(text)
        if df.empty:
            bot.sendMessage(chat_id=chat_id, text="❌ لم يتم العثور على توزيعات أرباح للسهم.", reply_to_message_id=msg_id)
            return "ok"

        last_dividend = df.iloc[-1]
        current_price = si.get_live_price(text)
        dividend_amount = last_dividend['dividend']
        ex_date = last_dividend.name.date()

        annual_yield = (dividend_amount * 4) / current_price * 100
        opportunity = annual_yield >= 5  # شرط بسيط لتحديد الفرصة

        result = f"""
📈 توزيعات أرباح سهم {text}

🔹 آخر توزيع: {dividend_amount} دولار
🔹 تاريخ الاستحقاق: {ex_date}
🔹 السعر الحالي: {round(current_price, 2)} دولار
🔹 العائد السنوي المتوقع: {round(annual_yield, 2)}%

📍 التوصية: {"✅ فرصة شراء" if opportunity else "❌ ليست فرصة حالياً"}
📍 نسبة تقييم الصفقة: {round(min(annual_yield, 10) * 10, 2)}%
        """
        bot.sendMessage(chat_id=chat_id, text=result, reply_to_message_id=msg_id)

        log_trade(
            symbol=text,
            strategy="dividend",
            entry_price=current_price,
            targets=None,
            stop_loss=None,
            score=round(min(annual_yield, 10) * 10, 2)
        )

    except Exception as e:
        bot.sendMessage(chat_id=chat_id, text=f"حدث خطأ أثناء التحليل: {e}", reply_to_message_id=msg_id)

    return "ok"

@app.route("/setwebhook", methods=["GET", "POST"])
def set_webhook():
    s = bot.setWebhook(f"https://<YOUR APP NAME>.onrender.com/{TOKEN}")
    return "webhook setup ok" if s else "webhook setup failed"

if __name__ == "__main__":
    app.run()
