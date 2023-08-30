from pyrogram import Client, filters
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, Message
import random
import time
from database import DatabaseManager
from character import CharacterManager
from pymongo import MongoClient

MONGO_URL = ("MONGO_URL")  # Retrieve MongoDB URI from Heroku environment variables

app = Client("my_bot")

# Connect to the database
mongo_client = pymongo.MongoClient(MONGO_URL)
db = mongo_client.get_database("anime_characters")


db_manager = DatabaseManager()
character_manager = CharacterManager()

user_harems = {}
spawn_time = 300  # Default spawn time in seconds

# Command to start the bot
@app.on_message(filters.command("start"))
def start(bot, message: Message):
    bot.send_message(message.chat.id, "Welcome to Character Collector Bot!")

# Collect a character by typing the name
@app.on_message(filters.text)
def collect_character(bot, message: Message):
    user_id = message.from_user.id
    character_name = message.text.strip()

    collected = collect_character_by_name(user_id, character_name)
    if collected:
        bot.send_message(message.chat.id, f"You collected {character_name}!")
    else:
        bot.send_message(message.chat.id, f"{character_name} not found.")

# Collect a character by name and add to the user's harem
def collect_character_by_name(user_id, character_name):
    character = character_manager.get_character_by_name(character_name)
    if character:
        if user_id not in user_harems:
            user_harems[user_id] = []
        user_harems[user_id].append(character)
        return True
    return False

# Inline query to search for characters
@app.on_inline_query()
def inline_query(bot, query):
    results = []

    if query.query:
        characters = db_manager.search_characters(query.query)
        for character in characters:
            description = f"Anime: {character['anime']} | Rank: {character['rank']}"
            results.append(
                InlineQueryResultArticle(
                    id=str(character['id']),
                    title=character['name'],
                    description=description,
                    input_message_content=InputTextMessageContent(
                        message_text=f"Character: {character['name']}\nAnime: {character['anime']}\nRank: {character['rank']}"
                    )
                )
            )

    bot.answer_inline_query(query.id, results=results, cache_time=1)

# Automatic character spawning in all chats
def spawn_characters_periodically():
    while True:
        for chat in app.get_dialogs():
            if chat.chat.type == "group" or chat.chat.type == "supergroup":
                spawn_random_character_img(app.send_photo, chat.chat.id)
        time.sleep(spawn_time)

if __name__ == "__main__":
    # Start the thread to spawn characters periodically
    import threading
    character_thread = threading.Thread(target=spawn_characters_periodically)
    character_thread.daemon = True
    character_thread.start()
    
    app.run()
