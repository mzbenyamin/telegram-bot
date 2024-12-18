//TELEGRAM_BOT_TOKEN

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import random

# پاسخ‌های جالب
funny_responses = [
    "تو چطور اینقدر باحالی؟ 😎",
    "من مثل یه ربات واقعی دارم صحبت می‌کنم، باور کن! 🤖",
    "چطوری من رو پیدا کردی؟ من دارم قایم میشم! 😂",
    "من نمی‌دونم چی بگم، ولی می‌دونم تو آدم باحالی هستی! 😁"
]

# دستورات ربات
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('سلام! من ربات باحال تلگرامی هستم. بگو ببینم چطوری می‌تونم بهت کمک کنم؟')

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('من می‌تونم به پیام‌های شما جواب‌های خلاقانه بدم. امتحان کن!')

# تابع برای پیام‌های تصادفی
def random_funny_response(update: Update, context: CallbackContext) -> None:
    response = random.choice(funny_responses)
    update.message.reply_text(response)

# اصلی‌ترین تابع
def main() -> None:
    # توکن ربات خودتون رو از BotFather بگیرید
    token = 'TELEGRAM_BOT_TOKEN'
    
    updater = Updater(token)

    dispatcher = updater.dispatcher

    # دستورات
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # پیام‌های عمومی
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, random_funny_response))

    # شروع ربات
    updater.start_polling()

    # ربات برای همیشه اجرا بمونه
    updater.idle()

if __name__ == '__main__':
    main()

