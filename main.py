from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from auth import is_authorized
from stock_analyzer import analyze_stock

TOKEN = "7250935830:AAEhcPifdrDk9Bxufd-rpsm2nM-cehkSAuk"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 مرحبًا! أرسل اسم السهم لتحليله.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if not is_authorized(user_id, text):
        await update.message.reply_text("🔐 أرسل كلمة المرور للمتابعة.")
        return

    if text.lower() == "ابدأ":
        await update.message.reply_text("✍️ أرسل اسم السهم (مثال: SLXN أو الراجحي)")
    else:
        result = analyze_stock(text)
        await update.message.reply_text(result)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
