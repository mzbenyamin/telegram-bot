# Telegram Bot: Web Scraper for Item Information

This project is a Python-based Telegram bot that scrapes item information from a website and provides the details to the user via the Telegram interface. It includes full documentation and is structured for easy deployment and uploading to GitHub.

## Features
- Accepts user input for searching items.
- Scrapes item details from a website using `requests` and `BeautifulSoup`.
- Sends the item image and details back to the user.
- Simple and easy-to-use Telegram bot interface.

## Prerequisites
Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher installed on your system.
- A Telegram bot token (you can get one from [BotFather](https://core.telegram.org/bots)).
- Libraries: `python-telegram-bot`, `requests`, `beautifulsoup4`. Install them using:

```bash
pip install python-telegram-bot requests beautifulsoup4
```

## Project Structure
```plaintext
.
├── main.py               # Main bot script
├── README.md             # Project documentation
└── requirements.txt      # Dependencies
```

## Installation
1. Clone the repository:

```bash
git clone https://github.com/yourusername/telegram-web-scraper-bot.git
cd telegram-web-scraper-bot
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Replace `YOUR_BOT_TOKEN` in `main.py` with your Telegram bot token.

4. Run the bot:

```bash
python main.py
```

## Usage
- Start the bot by sending `/start` in Telegram.
- Enter the name of the item you want to search.
- The bot will retrieve and send the item's details and image.

## Code
```python
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
```

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---
### Contributing
Feel free to fork this repository and submit pull requests for improvements or bug fixes.

### Issues
If you encounter any problems, please open an issue on GitHub.
