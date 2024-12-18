import os
import telebot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # گرفتن توکن از متغیر محیطی
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "سلام! ربات شما فعال شد!")

bot.polling()
