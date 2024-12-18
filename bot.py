from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ایجاد صفحه اولیه بازی
def create_board():
    board = [[" " for _ in range(3)] for _ in range(3)]
    return board

# تولید کلیدهای شیشه‌ای برای پنل
def generate_keyboard(board):
    keyboard = []
    for i in range(3):
        row = []
        for j in range(3):
            text = board[i][j] if board[i][j] != " " else "⬜"
            row.append(InlineKeyboardButton(text, callback_data=f"{i},{j}"))
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

# شروع بازی
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    board = create_board()
    context.user_data["board"] = board
    context.user_data["current_player"] = "❌"
    await update.message.reply_text(
        "بازی Tic Tac Toe شروع شد! نوبت بازیکن ❌",
        reply_markup=generate_keyboard(board),
    )

# مدیریت کلیک روی کلیدها
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    board = context.user_data["board"]
    current_player = context.user_data["current_player"]

    # خواندن موقعیت کلیک‌شده
    i, j = map(int, query.data.split(","))
    if board[i][j] == " ":
        board[i][j] = current_player
        context.user_data["current_player"] = "⭕" if current_player == "❌" else "❌"
    else:
        await query.edit_message_text(
            text="این خانه پر است! لطفاً جای دیگری کلیک کنید.",
            reply_markup=generate_keyboard(board),
        )
        return

    winner = check_winner(board)
    if winner:
        await query.edit_message_text(
            text=f"بازیکن {winner} برنده شد! 🎉",
            reply_markup=generate_keyboard(board),
        )
        return

    if all(cell != " " for row in board for cell in row):
        await query.edit_message_text(
            text="بازی مساوی شد! 🤝",
            reply_markup=generate_keyboard(board),
        )
        return

    await query.edit_message_text(
        text=f"نوبت بازیکن {context.user_data['current_player']}",
        reply_markup=generate_keyboard(board),
    )

# بررسی برنده بازی
def check_winner(board):
    # بررسی خطوط افقی و عمودی
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != " ":
            return board[0][i]
    # بررسی قطرها
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    return None

# راه‌اندازی ربات
def main():
    application = Application.builder().token("8011536409:AAGUT4m9BFxnQxppgBtbIrMXV-wF19txobs").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_polling()

if __name__ == "__main__":
    main()
