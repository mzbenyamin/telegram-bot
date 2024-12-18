from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import random

# متغیر سراسری برای ذخیره عدد تصادفی
random_number = None

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('سلام! من یک عدد تصادفی بین 1 تا 100 انتخاب می‌کنم. حدس بزن!')

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('من می‌توانم یک عدد تصادفی برای تو انتخاب کنم و تو باید حدس بزنی. با هر حدسی که می‌زنی، من بهت می‌گم که بالاتر یا پایین‌تره!')

# شروع بازی حدس‌زدن عدد
def guess_game(update: Update, context: CallbackContext) -> None:
    global random_number
    random_number = random.randint(1, 100)  # انتخاب یک عدد تصادفی بین 1 تا 100
    update.message.reply_text("بازی شروع شد! حدس بزن عدد من چیه؟ بین 1 تا 100!")

# پاسخ به حدس‌ها
def check_guess(update: Update, context: CallbackContext) -> None:
    global random_number
    if random_number is None:
        update.message.reply_text("برای شروع بازی، دستور /guess رو وارد کن!")
        return

    try:
        user_guess = int(update.message.text)
    except ValueError:
        update.message.reply_text("لطفاً فقط یک عدد وارد کن!")
        return

    if user_guess < random_number:
        update.message.reply_text("عدد من بزرگتره! دوباره حدس بزن.")
    elif user_guess > random_number:
        update.message.reply_text("عدد من کوچیک‌تره! دوباره حدس بزن.")
    else:
        update.message.reply_text("آفرین! درست حدس زدی. بازی دوباره شروع شد!")
        random_number = None  # بازی تمام می‌شود و عدد جدید برای بازی بعدی نیاز است

# دستورات ربات
def main() -> None:
    token = '8011536409:AAGUT4m9BFxnQxppgBtbIrMXV-wF19txobs'  # توکن ربات

    updater = Updater(token)
    dispatcher = updater.dispatcher

    # دستورات
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("guess", guess_game))

    # دریافت پیام‌های عددی از کاربر
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, check_guess))

    # شروع ربات
    updater.start_polling()

    # ربات برای همیشه اجرا بمونه
    updater.idle()

if __name__ == '__main__':
    main()
