import telebot
import os

# Token من BotFather
TOKEN = os.getenv("BOT_TOKEN")  # تأكد من إضافته في Render

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلًا بك في بوت تحليل الأسهم 🔍\nأرسل اسم السهم لبدء التحليل.")

@bot.message_handler(func=lambda message: True)
def analyze_stock(message):
    stock_symbol = message.text.strip().upper()

    try:
        # نتيجة تحليل وهمية كمثال - استبدلها بالتحليل الرقمي والفني الحقيقي
        result = (
            f"\n📊 تحليل السهم: {stock_symbol}\n"
            f"✅ التقييم: 92%\n"
            f"🎯 الأهداف: 56.3 - 58.1 - 60.0\n"
            f"🔍 شرعية السهم: متوافقة ✅\n"
            f"📈 المؤشرات: صاعدة\n"
            f"📰 الأخبار المؤثرة: لا توجد حالياً\n"
            f"\n🔁 إذا تغيرت الظروف، ستصلك تنبيهات."
        )

        bot.reply_to(message, result)

    except Exception as e:
        bot.reply_to(message, "حدث خطأ أثناء تحليل السهم ❌")

# بدء البوت
print("البوت يعمل الآن...")
bot.infinity_polling()
