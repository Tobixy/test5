import threading
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, InputTextMessageContent, InlineQueryResultArticle
from main import app
from database import DatabaseManager

db_manager = DatabaseManager()


# Command to show top 10 harem collectors and user's own harem
@app.on_message(filters.command("harem"))
def check_harem(bot, message: Message):
    user_id = message.from_user.id
    harem = db_manager.get_user_harem(user_id)
    
    top_collectors = db_manager.get_top_harem_collectors(limit=10)
    top_collectors_str = "\n".join([f"{idx+1}. {user}: {count} characters" for idx, (user, count) in enumerate(top_collectors)])
    
    if harem:
        harem_list = "\n".join(harem)
        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Check Your Harem", switch_inline_query_current_chat="/harem")],
            [InlineKeyboardButton("Cancel", callback_data="cancel")]
        ])
        bot.send_message(message.chat.id, f"Top 10 Collectors:\n{top_collectors_str}\n\nYour harem:\n{harem_list}", reply_markup=inline_keyboard)
    else:
        inline_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Check Your Harem", switch_inline_query_current_chat="/harem")],
            [InlineKeyboardButton("Cancel", callback_data="cancel")]
        ])
        bot.send_message(message.chat.id, f"Top 10 Collectors:\n{top_collectors_str}\n\nYour harem is empty.", reply_markup=inline_keyboard)
