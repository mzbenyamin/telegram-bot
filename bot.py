import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext
import sympy as sp

# توکن ربات تلگرام خودتون رو اینجا وارد کنید
TELEGRAM_TOKEN = "8011536409:AAGUT4m9BFxnQxppgBtbIrMXV-wF19txobs"

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
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_input = update.message.text
    solution = solve_math_problem(user_input)
    await update.message.reply_text(f"نتیجه: {solution}")

# تابع main برای راه‌اندازی ربات
def main() -> None:
    # ایجاد Application و ربات با توکن
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # هندلر برای پیام‌های متنی
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # شروع ربات
    application.run_polling()

if __name__ == '__main__':
    main()
