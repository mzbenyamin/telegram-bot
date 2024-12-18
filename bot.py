
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

# تابع استخراج آیتم‌ها از سایت Platopedia
def extract_item_details():
    url = "https://platopedia.com/items"
    response = requests.get(url)

    # بررسی موفقیت‌آمیز بودن درخواست
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # استخراج نام آیتم
        item_name = soup.select_one("#popup-item > div > div > div.modal-header.text-center > h4")
        item_name = item_name.text.strip() if item_name else "نامی یافت نشد"

        # استخراج ارزش آیتم
        item_value = soup.select_one("#popup-item > div > div > div.modal-body > table > tbody > tr:nth-child(3) > td:nth-child(2)")
        item_value = item_value.text.strip() if item_value else "ارزش یافت نشد"

        # استخراج عکس آیتم
        item_image = soup.select_one("#popup-item > div > div > div.modal-body > div > div > img")
        item_image_url = item_image['src'] if item_image else "عکس یافت نشد"

        # نمایش اطلاعات استخراج‌شده
        return {
            "name": item_name,
            "value": item_value,
            "image": item_image_url
        }
    else:
        return "مشکلی در درخواست به سایت پیش آمده."

# دستور start برای شروع ربات
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("سلام! لطفاً چیزی که می‌خواهید جستجو کنید رو بنویسید.")

# دریافت پیام و جستجو در سایت
async def handle_message(update: Update, context: CallbackContext):
    query = update.message.text
    item_details = extract_item_details()
await update.message.reply_text(f"""نام آیتم: {item_details['name']}
ارزش آیتم: {item_details['value']}
تصویر: {item_details['image']}""")

# اصلی‌ترین فانکشن برای راه‌اندازی ربات
def main():
    app = ApplicationBuilder().token('8011536409:AAGUT4m9BFxnQxppgBtbIrMXV-wF19txobs').build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
