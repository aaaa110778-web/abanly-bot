import re
import os
from flask import Flask, request
import telegram
import yahoo_fin.stock_info as si
import pandas as pd
from trade_logger.logger import log_trade, update_trade_result

app = Flask(__name__)
TOKEN = os.environ.get("BOT_TOKEN")
bot = telegram.Bot(token=TOKEN)

@app.route('/')
def index():
    return 'Fundamental Analysis Bot is running.'

@app.route(f'/{TOKEN}', methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    msg_id = update.message.message_id
    text = update.message.text.strip().upper()

    if text == "/START":
        bot.sendMessage(chat_id=chat_id, text="مرحباً بك في بوت التحليل الأساسي للأسهم!", reply_to_message_id=msg_id)
        return 'ok'

    try:
        symbol = re.sub(r'\W+', '', text)
        print(f"Fetching data for {symbol}")
        data = si.get_quote_table(symbol)
        stats = si.get_stats_valuation(symbol)
        stats_df = pd.concat([si.get_stats(symbol), stats])

        indicators = {}
        indicators['السعر الحالي'] = data.get('Previous Close', 'N/A')
        indicators['P/E'] = data.get('PE Ratio (TTM)', 'N/A')
        indicators['P/B'] = _get_val(stats_df, 'Price/Book (mrq)')
        indicators['PEG'] = _get_val(stats_df, 'PEG Ratio (5 yr expected) 1')
        indicators['ROA'] = _get_val(stats_df, 'Return on assets')
        indicators['ROE'] = _get_val(stats_df, 'Return on equity')
        indicators['Debt/Equity'] = _get_val(stats_df, 'Total debt/equity')

        # تقييم الصفقة
        score = 0
        checks = {
            'P/E': lambda v: float(v) < 25,
            'P/B': lambda v: float(v) < 3,
            'PEG': lambda v: float(v) <= 1.5,
            'ROA': lambda v: float(v.strip('%')) > 5,
            'ROE': lambda v: float(v.strip('%')) > 15,
            'Debt/Equity': lambda v: float(v) < 1
        }

        for key, func in checks.items():
            try:
                if func(indicators[key]):
                    score += 1
            except:
                continue

        score_percentage = round((score / len(checks)) * 100, 2)

        # عرض النتيجة
        result = f"""
📊 التحليل الأساسي لسهم {symbol}

🔹 السعر الحالي: {indicators['السعر الحالي']} دولار
🔹 مضاعف الربحية (P/E): {indicators['P/E']}
🔹 مضاعف القيمة الدفترية (P/B): {indicators['P/B']}
🔹 PEG: {indicators['PEG']}
🔹 العائد على الأصول (ROA): {indicators['ROA']}
🔹 العائد على حقوق المساهمين (ROE): {indicators['ROE']}
🔹 نسبة الدين إلى حقوق الملكية: {indicators['Debt/Equity']}

📍 نسبة تقييم الصفقة: {score_percentage}%
        """
        bot.sendMessage(chat_id=chat_id, text=result, reply_to_message_id=msg_id)

        # تسجيل الصفقة
        entry_price = indicators['السعر الحالي']
        if entry_price != 'N/A':
            log_trade(
                symbol=symbol,
                strategy="fundamental",
                entry_price=float(entry_price),
                targets=None,
                stop_loss=None,
                score=score_percentage
            )

    except Exception as e:
        bot.sendMessage(chat_id=chat_id, text=f"حدث خطأ أثناء التحليل: {e}", reply_to_message_id=msg_id)

    return 'ok'

def _get_val(df, colname):
    try:
        return df[df.iloc[:, 0].str.contains(colname, case=False)].iloc[0, 1]
    except:
        return "N/A"

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook(f"https://<YOUR APP NAME>.onrender.com/{TOKEN}")
    return "webhook setup ok" if s else "webhook setup failed"

if __name__ == '__main__':
    app.run()
