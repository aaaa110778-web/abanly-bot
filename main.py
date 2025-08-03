import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from utils import analyze_stock
from password_guard import check_password, set_password_for_today
from datetime import datetime

# إعدادات البوت
TOKEN = "7250935830:AAEhcPifdrDk9Bxufd-rpsm2nM-cehkSAuk"
PASSWORD = "123123"

# المعالجة الرئيسية للرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()

    if not check_password(update.effective_user.id):
        if user_input == PASSWORD:
            set_password_for_today(update.effective_user.id)
            await update.message.reply_text("✅ تم تسجيل الدخول بنجاح لليوم.")
        else:
            await update.message.reply_text("🔒 أدخل كلمة المرور الصحيحة لاستخدام البوت.")
        return

    await update.message.reply_text("🔍 جارٍ تحليل السهم...")
    result = analyze_stock(user_input)
    await update.message.reply_text(result)

# بدء التشغيل
def main():
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()