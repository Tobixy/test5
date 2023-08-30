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


# Command to initiate a gift
@app.on_message(filters.command("gift"))
def initiate_gift(bot, message: Message):
    user_id = message.from_user.id
    if len(message.command) != 2:
        bot.send_message(message.chat.id, "Please use /gift character_id to initiate a gift.")
        return
    
    character_id = message.command[1]
    harem = db_manager.get_user_harem(user_id)
    
    if character_id not in harem:
        bot.send_message(message.chat.id, "You don't have that character in your harem.")
        return
    
    inline_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Accept Gift", callback_data=f"accept_gift_{user_id}_{character_id}"),
         InlineKeyboardButton("Cancel", callback_data="cancel")]
    ])
    bot.send_message(message.chat.id, f"Are you sure you want to gift character {character_id}?", reply_markup=inline_keyboard)

# Command to initiate a trade
@app.on_message(filters.command("trade"))
def initiate_trade(bot, message: Message):
    user_id = message.from_user.id
    if len(message.command) != 3:
        bot.send_message(message.chat.id, "Please use /trade your_character_id their_character_id to initiate a trade.")
        return
    
    your_character_id = message.command[1]
    their_character_id = message.command[2]
    
    your_harem = db_manager.get_user_harem(user_id)
    if your_character_id not in your_harem:
        bot.send_message(message.chat.id, "You don't have the first character in your harem.")
        return
    
    inline_keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Accept Trade", callback_data=f"accept_trade_{user_id}_{your_character_id}_{their_character_id}"),
         InlineKeyboardButton("Cancel", callback_data="cancel")]
    ])
    bot.send_message(message.chat.id, f"Are you sure you want to trade character {your_character_id} for character {their_character_id}?", reply_markup=inline_keyboard)

# Callback to handle gift and trade accept or cancel
@app.on_callback_query()
def handle_inline_buttons(bot, callback_query: CallbackQuery):
    data = callback_query.data.split("_")
    action = data[0]
    
    if action == "accept_gift":
        user_id = int(data[1])
        character_id = data[2]
        
        user_chat_id = callback_query.from_user.id
        harem = db_manager.get_user_harem(user_id)
        
        if user_chat_id != user_id or character_id not in harem:
            bot.answer_callback_query(callback_query.id, text="Invalid request.")
            return
        
        db_manager.transfer_character(user_id, user_chat_id, character_id)
        bot.answer_callback_query(callback_query.id, text="Gift accepted!")
        
    elif action == "accept_trade":
        your_user_id = int(data[1])
        your_character_id = data[2]
        their_character_id = data[3]
        
        your_user_chat_id = callback_query.from_user.id
        your_harem = db_manager.get_user_harem(your_user_id)
        
        if your_user_chat_id != your_user_id or your_character_id not in your_harem:
            bot.answer_callback_query(callback_query.id, text="Invalid trade request.")
            return
        
        their_user_id = callback_query.message.reply_to_message.from_user.id
        their_harem = db_manager.get_user_harem(their_user_id)
        
        if their_character_id not in their_harem:
            bot.answer_callback_query(callback_query.id, text="Invalid trade request.")
            return
        
        db_manager.trade_characters(your_user_id, their_user_id, your_character_id, their_character_id)
        bot.answer_callback_query(callback_query.id, text="Trade accepted!")

    elif action == "cancel":
        bot.answer_callback_query(callback_query.id, text="Action canceled.")

# ... (rest of the code)
