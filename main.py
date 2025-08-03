import telebot
import datetime

API_KEY = '7250935830:AAEhcPifdrDk9Bxufd-rpsm2nM-cehkSAuk'
bot = telebot.TeleBot(API_KEY)

PASSWORD = "123123"
authorized_users = {}

def is_authorized(user_id):
    today = datetime.date.today()
    return authorized_users.get(user_id) == today

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if is_authorized(message.from_user.id):
        bot.reply_to(message, "مرحبًا، أرسل اسم السهم فقط.")
    else:
        bot.reply_to(message, "🚫 أدخل كلمة السر:")

@bot.message_handler(func=lambda m: not is_authorized(m.from_user.id))
def check_password(message):
    if message.text == PASSWORD:
        authorized_users[message.from_user.id] = datetime.date.today()
        bot.reply_to(message, "✅ تم التحقق! أرسل اسم السهم الآن.")
    else:
        bot.reply_to(message, "❌ كلمة السر غير صحيحة.")

@bot.message_handler(func=lambda m: is_authorized(m.from_user.id))
def analyze_stock(message):
    stock_name = message.text.upper()

    price = 25.50
    up_trend = 27.15
    down_trend = 20.82
    rsi = 62
    ma = 24.13

    diff = (up_trend - down_trend) / 24
    levels = [round(down_trend + diff * i, 2) for i in range(1, 25)]
    nearest = next((lvl for lvl in levels if lvl > price), None)
    next_goals = levels[levels.index(nearest):][:3]

    response = f"""
📊 تحليل سهم: {stock_name}
🔹 السعر الحالي: {price}
🔹 الترند الصاعد: {up_trend}
🔹 الترند الهابط: {down_trend}
🔹 أقرب أهداف:
• {next_goals[0]}  
• {next_goals[1]}  
• {next_goals[2]}

📈 RSI: {rsi}
📉 MA: {ma}

🔍 المؤشر العام: إذا وصل 11080، يتوقع أن يصل السهم إلى {next_goals[0]}
✅ شرعي حسب يقين
📊 تقييم الصفقة: 85%
"""
    bot.reply_to(message, response)

bot.polling()
