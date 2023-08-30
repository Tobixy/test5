from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from main import app
from database import DatabaseManager

db_manager = DatabaseManager()

# Command to show the top 10 collectors leaderboard
@app.on_message(filters.command("leaderboard"))
def show_leaderboard(bot, message):
    top_collectors = db_manager.get_top_harem_collectors(limit=10)
    top_collectors_str = "\n".join([f"{idx+1}. {user}: {count} characters" for idx, (user, count) in enumerate(top_collectors)])
    
    inline_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("View Profile", switch_inline_query_current_chat="/profile")],
        [InlineKeyboardButton("Cancel", callback_data="cancel")]
    ])
    bot.send_message(message.chat.id, f"Top 10 Collectors:\n{top_collectors_str}", reply_markup=inline_keyboard)

# Callback to handle profile view
@app.on_callback_query()
def handle_inline_buttons(bot, callback_query: CallbackQuery):
    data = callback_query.data.split("_")
    action = data[0]
    
    if action == "profile":
        user_id = callback_query.from_user.id
        harem = db_manager.get_user_harem(user_id)
        
        if not harem:
            bot.answer_callback_query(callback_query.id, text="Your harem is empty.")
            return
        
        harem_list = "\n".join(harem)
        bot.send_message(user_id, f"Your harem:\n{harem_list}")

    elif action == "cancel":
        bot.answer_callback_query(callback_query.id, text="Action canceled.")
