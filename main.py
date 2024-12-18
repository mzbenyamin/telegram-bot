
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, CallbackContext
import sqlite3

# Database setup
DB_PATH = "game.db"
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY,
        username TEXT,
        money INTEGER DEFAULT 1000,
        businesses TEXT DEFAULT ''
    )''')
    conn.commit()
    conn.close()

# Start command
async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Add player to database if not exists
    c.execute("SELECT * FROM players WHERE id=?", (user.id,))
    player = c.fetchone()
    if not player:
        c.execute("INSERT INTO players (id, username) VALUES (?, ?)", (user.id, user.username))
        conn.commit()
        await update.message.reply_text(f"به بازی تجارت مجازی خوش اومدی، {user.username}!")
    else:
        await update.message.reply_text(f"خوش اومدی، {user.username}! وضعیتت رو با /status ببین.")
    
    conn.close()

# Buy command
async def buy(update: Update, context: CallbackContext):
    businesses = {
        "فروشگاه": {"price": 1000, "profit": 100},
        "کارخانه": {"price": 5000, "profit": 500},
        "صرافی": {"price": 10000, "profit": 1500},
    }
    
    if len(context.args) == 0:
        await update.message.reply_text("فرمت صحیح: /buy [نام کسب‌وکار]
کسب‌وکارهای موجود: فروشگاه، کارخانه، صرافی")
        return

    business_name = context.args[0]
    if business_name not in businesses:
        await update.message.reply_text("کسب‌وکار نامعتبره! فقط فروشگاه، کارخانه یا صرافی رو می‌تونی بخری.")
        return
    
    user = update.effective_user
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Check user's balance
    c.execute("SELECT money, businesses FROM players WHERE id=?", (user.id,))
    player = c.fetchone()
    if not player:
        await update.message.reply_text("لطفاً اول دستور /start رو بزن!")
        conn.close()
        return
    
    money, owned_businesses = player
    business_price = businesses[business_name]["price"]

    if money < business_price:
        await update.message.reply_text("پولت کافی نیست! بیشتر تلاش کن.")
    else:
        # Deduct money and add business
        new_money = money - business_price
        new_businesses = f"{owned_businesses},{business_name}" if owned_businesses else business_name
        c.execute("UPDATE players SET money=?, businesses=? WHERE id=?", (new_money, new_businesses, user.id))
        conn.commit()
        await update.message.reply_text(f"تبریک! {business_name} رو خریدی. موجودی جدیدت: {new_money}.")

    conn.close()

# Status command
async def status(update: Update, context: CallbackContext):
    user = update.effective_user
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT money, businesses FROM players WHERE id=?", (user.id,))
    player = c.fetchone()
    if not player:
        await update.message.reply_text("لطفاً اول دستور /start رو بزن!")
    else:
        money, businesses = player
        businesses_list = businesses.split(",") if businesses else ["هیچ کسب‌وکاری نداری!"]
        businesses_text = "\n".join(businesses_list)
        await update.message.reply_text(f"وضعیت فعلی:
موجودی: {money}\nکسب‌وکارها:
{businesses_text}")

    conn.close()

# Main function
def main():
    init_db()
    app = ApplicationBuilder().token("8011536409:AAGUT4m9BFxnQxppgBtbIrMXV-wF19txobs").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CommandHandler("status", status))
    app.run_polling()

if __name__ == "__main__":
    main()
