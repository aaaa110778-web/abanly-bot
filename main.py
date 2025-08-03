import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from stock_analyzer import analyze_stock
from  auth import is_authorized, authorize_user
from auth import load_authorized_users  # تحميل المستخدمين المحفوظين

# إعدادات البوت
TOKEN = "7250935830:AAEhcPifdrDk9Bxufd-rpsm2n-cehkSAuk"
PASSWORD = "123123"

# المعالجة الرئيسية للرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()

    if not is_authorized(update.effective_user.id):
        if user_input == PASSWORD:
            authorize_user(update.effective_user.id)
            await update.message.reply_text("✅ تم تسجيل الدخول بنجاح لليوم.")
        else:
            await update.message.reply_text("🔒 أدخل كلمة المرور الصحيحة لاستخدام البوت.")
        return

    await update.message.reply_text("🔍 جارٍ تحليل السهم...")
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, analyze_stock, user_input)
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ أثناء التحليل:\n{str(e)}")

# بدء التشغيل
def main():
    logging.basicConfig(level=logging.INFO)
    load_authorized_users()  # تحميل صلاحيات اليوم
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
