import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from auth import is_authorized, authorize_user, load_authorized_users
from stock_analyzer import analyze_stock

TOKEN = "ضع التوكن هنا"
PASSWORD = "123123"

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
        result = analyze_stock(user_input)
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ: {e}")

def main():
    logging.basicConfig(level=logging.INFO)
    load_authorized_users()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
