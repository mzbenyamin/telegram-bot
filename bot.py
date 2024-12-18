import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import sympy as sp

# توکن ربات تلگرام خودتون رو اینجا وارد کنید
TELEGRAM_TOKEN = 'TELEGRAM_BOT_TOKEN'

# تنظیمات لاگ برای ردیابی خطاها
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# تابعی برای حل مسائل ریاضی
def solve_math_problem(problem: str):
    try:
        # تبدیل رشته به فرمول ریاضی
        result = sp.sympify(problem)
        return result
    except Exception as e:
        return f"خطا در حل معادله: {e}"

# هنگامی که کاربر پیام می‌فرسته
def handle_message(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    solution = solve_math_problem(user_input)
    update.message.reply_text(f"نتیجه: {solution}")

# تابع main برای راه‌اندازی ربات
def main() -> None:
    # ایجاد Updater و ربات با توکن
    updater = Updater(TELEGRAM_TOKEN)

    # دریافت dispatcher برای ثبت هندلرها
    dispatcher = updater.dispatcher

    # هندلر برای پیام‌های متنی
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # شروع ربات
    updater.start_polling()

    # ربات همیشه در حال فعالیت باشه
    updater.idle()

if __name__ == '__main__':
    main()
