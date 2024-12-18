from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# توکن ربات تلگرام شما
TELEGRAM_TOKEN = 'TELEGRAM_BOT_TOKEN'

# تابعی برای پاسخ دادن به پیام‌ها
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("سلام به ربات من خوش اومدید!")

# تابع اصلی که ربات رو اجرا می‌کنه
def main() -> None:
    # ایجاد Updater و ربات با توکن
    updater = Updater(TELEGRAM_TOKEN)

    # دریافت dispatcher برای ثبت هندلرها
    dispatcher = updater.dispatcher

    # هندلر برای فرمان /start
    dispatcher.add_handler(CommandHandler("start", start))

    # هندلر برای پیام‌های متنی
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, start))

    # شروع ربات
    updater.start_polling()

    # ربات همیشه در حال فعالیت باشه
    updater.idle()

if __name__ == '__main__':
    main()
