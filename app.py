import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# ضع التوكنات الخاصة بك هنا
BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
STOCKDATA_API_KEY = 'YOUR_STOCKDATA_API_KEY'

# دالة لجلب السعر الفوري
def get_stock_price(symbol):
    url = f"https://api.stockdata.org/v1/data/quote?symbols={symbol}&api_token={STOCKDATA_API_KEY}"
    response = requests.get(url)
    data = response.json()
    try:
        price = data["data"][0]["price"]
        return f"📈 السعر الحالي لسهم {symbol.upper()} هو: {price} $"
    except:
        return "❌ لم يتم العثور على بيانات لهذا السهم."

# دالة أمر /price
def price_command(update: Update, context: CallbackContext):
    if not context.args:
        update.message.reply_text("اكتب اسم السهم بعد الأمر مثل: /price AAPL")
        return
    symbol = context.args[0].upper()
    message = get_stock_price(symbol)
    update.message.reply_text(message)

# إعداد البوت
updater = Updater(BOT_TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler("price", price_command))

# تشغيل البوت
updater.start_polling()
updater.idle()
