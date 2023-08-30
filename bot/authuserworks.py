from pyrogram import filters
from pyrogram.types import Message
from main import app
from database import DatabaseManager
from auth import DEVELOPER_USERS, AUTHORIZED_USERS

db_manager = DatabaseManager()

def is_developer(user_id):
    return str(user_id) in DEVELOPER_USERS

def is_authorized(user_id):
    return str(user_id) in AUTHORIZED_USERS

# Command to add character with image
@app.on_message(filters.command("add_character_img") & filters.user(is_authorized))
def add_character_img(bot, message: Message):
    user_id = message.from_user.id
    
    # Check if a photo is attached
    if message.photo:
        photo_id = message.photo[-1].file_id
        caption = message.caption or ""
        parts = caption.split("\n")
        
        # Parse character information from caption
        if len(parts) >= 3:
            character_name = parts[0]
            rank = parts[1]
            anime_name = parts[2]
            
            # Save character details to the database
            character_id = db_manager.add_character_with_image(character_name, rank, anime_name, photo_id)
            
            # Reply to the user with a success message
            bot.send_message(message.chat.id, f"Character added successfully!\nID: {character_id}")
        else:
            bot.send_message(message.chat.id, "Invalid caption format. Please provide:\nCharacter Name\nRank\nAnime Name")
    else:
        bot.send_message(message.chat.id, "Please attach a photo and provide a caption.")

# Command to reset user harem
@app.on_message(filters.command("reset_harem") & filters.user(is_developer))
def reset_harem(bot, message: Message):
    user_id = int(message.text.split()[1])
    db_manager.reset_user_harem(user_id)
    
    bot.send_message(message.chat.id, f"Harem for user {user_id} reset successfully!")
