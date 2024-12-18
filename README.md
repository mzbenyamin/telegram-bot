
# Telegram Tycoon Game Bot

## Description
This is a Telegram bot game where players can build virtual businesses, earn money, and compete with others.

## How to Run
1. Install dependencies:
   ```
   pip install python-telegram-bot
   ```
2. Add your Telegram bot token in `main.py` by replacing `YOUR_BOT_TOKEN`.
3. Run the bot:
   ```
   python main.py
   ```
4. Use the following commands in Telegram:
   - `/start`: Start the game.
   - `/buy [business_name]`: Buy a business (e.g., `/buy فروشگاه`).
   - `/status`: Check your balance and businesses.

## File Structure
- `main.py`: The main bot code.
- `game.db`: SQLite database for storing player data.
