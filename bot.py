import requests
from bs4 import BeautifulSoup
from telegram import Update, Bot, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

def start(update: Update, context: CallbackContext):
    update.message.reply_text("سلام! برای دریافت اطلاعات، نام آیتم مورد نظر خود را وارد کنید.")

def search_item(update: Update, context: CallbackContext):
    query = update.message.text.strip()
    url = "https://platopedia.com/items"
    
    try:
        # ارسال درخواست به سایت با پارامتر جستجو
        response = requests.get(url, params={"search": query})
        if response.status_code != 200:
            update.message.reply_text("خطا در دسترسی به سایت. لطفاً دوباره تلاش کنید.")
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        # استخراج لینک آیتم
        item_link = soup.select_one("a[href*='/items/"])
        if not item_link:
            update.message.reply_text("هیچ آیتمی با این نام یافت نشد.")
            return

        # استخراج اطلاعات از صفحه جزئیات آیتم
        item_url = item_link['href']
        item_response = requests.get(item_url)
        item_soup = BeautifulSoup(item_response.text, 'html.parser')

        # استخراج جزئیات آیتم
        name = item_soup.select_one("#popup-item > div > div > div.modal-header.text-center > h4").text.strip()
        category = item_soup.select_one("#popup-item > div > div > div.modal-body > table > tbody > tr:nth-child(1) > td:nth-child(2)").text.strip()
        value = item_soup.select_one("#popup-item > div > div > div.modal-body > table > tbody > tr:nth-child(3) > td:nth-child(2) > font").text.strip()
        details = item_soup.select_one("#popup-item > div > div > div.modal-body > table > tbody > tr:nth-child(4) > td:nth-child(2)").text.strip()
        link = item_soup.select_one("#popup-item > div > div > div.modal-body > table > tbody > tr:nth-child(5) > td:nth-child(2)").text.strip()
        image_url = item_soup.select_one("#popup-item > div > div > div.modal-body > div:nth-child(2) > div > img")['src']

        # دانلود عکس آیتم
        image_response = requests.get(image_url, stream=True)
        if image_response.status_code == 200:
            bot = Bot(context.bot.token)
            bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=image_response.content,
                caption=(
                    f"\U0001F4D6 نام: {name}\n"
                    f"\U0001F4C2 دسته‌بندی: {category}\n"
                    f"\U0001F4B0 ارزش آیتم: {value}\n"
                    f"\U0001F4D1 اطلاعات آیتم: {details}\n"
                    f"\U0001F517 لینک آیتم: {link}"
                )
            )
        else:
            update.message.reply_text("خطا در دانلود تصویر آیتم.")
    
    except Exception as e:
        update.message.reply_text(f"خطا: {e}")

def main():
    # جایگزین کردن 'YOUR_BOT_TOKEN' با توکن ربات تلگرام
    updater = Updater("YOUR_BOT_TOKEN")

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, search_item))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
