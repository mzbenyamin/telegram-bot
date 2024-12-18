# TELEGRAM_BOT_TOKEN
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import random

# پاسخ‌های جالب
funny_responses = [
    "تو چطور اینقدر باحالی؟ 😎",
    "من مثل یه ربات واقعی دارم صحبت می‌کنم، باور کن! 🤖",
    "چطوری من رو پیدا کردی؟ من دارم قایم میشم! 😂",
    "من نمی‌دونم چی بگم، ولی می‌دونم تو آدم باحالی هستی! 😁"
]

# دستورات ربات
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('سلام! من ربات باحال تلگرامی هستم. بگو ببینم چطوری می‌تونم بهت کمک کنم؟')

async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('من می‌تونم به پیام‌های شما جواب‌های خلاقانه بدم. امتحان کن!')

# تابع برای پیام‌های تصادفی
async def random_funny_response(update: Update, context: CallbackContext) -> None:
    response = random.choice(funny_responses)
    await update.message.reply_text(response)

# اصلی‌ترین تابع
def main() -> None:
    # توکن ربات خودتون رو از BotFather بگیرید
    token = 'TELEGRAM_BOT_TOKEN'
    
    # ایجاد Application
    application = Application.builder().token(token).build()

    # دستورات
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # پیام‌های عمومی
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, random_funny_response))

    # شروع ربات
    application.run_polling()

if __name__ == '__main__':
    main()
