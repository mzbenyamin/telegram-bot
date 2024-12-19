from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import requests
from bs4 import BeautifulSoup

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! برای دریافت اطلاعات، نام آیتم مورد نظر خود را وارد کنید.")

async def search_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.strip()
    url = "https://platopedia.com/items"

    try:
        response = requests.get(url, params={"search": query})
        if response.status_code != 200:
            await update.message.reply_text("خطا در دسترسی به سایت. لطفاً دوباره تلاش کنید.")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        item_link = soup.select_one("a[href*='/items/']")
        if not item_link:
            await update.message.reply_text("هیچ آیتمی با این نام یافت نشد.")
            return

        item_url = item_link['href']
        item_response = requests.get(item_url)
        item_soup = BeautifulSoup(item_response.text, 'html.parser')

        name = item_soup.select_one("#popup-item > div > div > div.modal-header.text-center > h4").text.strip()
        category = item_soup.select_one("#popup-item > div > div > div.modal-body > table > tbody > tr:nth-child(1) > td:nth-child(2)").text.strip()
        value = item_soup.select_one("#popup-item > div > div > div.modal-body > table > tbody > tr:nth-child(3) > td:nth-child(2) > font").text.strip()
        details = item_soup.select_one("#popup-item > div > div > div.modal-body > table > tbody > tr:nth-child(4) > td:nth-child(2)").text.strip()
        link = item_soup.select_one("#popup-item > div > div > div.modal-body > table > tbody > tr:nth-child(5) > td:nth-child(2)").text.strip()
        image_url = item_soup.select_one("#popup-item > div > div > div.modal-body > div:nth-child(2) > div > img")['src']

        image_response = requests.get(image_url, stream=True)
        if image_response.status_code == 200:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=image_response.content,
                caption=(
                    f"📖 نام: {name}\n"
                    f"📂 دسته‌بندی: {category}\n"
                    f"💰 ارزش آیتم: {value}\n"
                    f"📝 اطلاعات آیتم: {details}\n"
                    f"🔗 لینک آیتم: {link}"
                )
            )
        else:
            await update.message.reply_text("خطا در دانلود تصویر آیتم.")
    except Exception as e:
        await update.message.reply_text(f"خطا: {e}")

def main():
    application = Application.builder().token("8011536409:AAGUT4m9BFxnQxppgBtbIrMXV-wF19txobs").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_item))
    application.run_polling()

if __name__ == "__main__":
    main()
