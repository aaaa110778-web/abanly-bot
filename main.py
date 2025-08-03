from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# توكن البوت
TOKEN = "7250935830:AAEhcPifdrDk9Bxufd-rpsm2nM-cehkSAuk"

# دالة بدء البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 مرحبًا! البوت يعمل الآن.\nأرسل اسم السهم للتحليل.")

# النقطة الرئيسية لتشغيل البوت
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # إضافة أمر /start
    app.add_handler(CommandHandler("start", start))

    # بدء التشغيل المستمر
    app.run_polling()

if __name__ == "__main__":
    main()
