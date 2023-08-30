from pyrogram import filters
from pyrogram.types import Message
from main import app, AUTHORIZED_USERS

class AnimeCharacterManager:
    def __init__(self):
        self.anime_characters = []

    def add_anime_character(self, character_info):
        self.anime_characters.append(character_info)

anime_character_manager = AnimeCharacterManager()

@app.on_message(filters.command("add_anime_character") & filters.user(AUTHORIZED_USERS))
async def add_anime_character_handler(_, message: Message):
    if len(message.command) < 4:
        await message.reply("Please provide character name, rank, and anime name.")
        return

    character_name = message.command[1]
    rank = message.command[2]
    anime_name = message.command[3]
    character_info = {"name": character_name, "rank": rank, "anime": anime_name}

    anime_character_manager.add_anime_character(character_info)
    await message.reply("Anime character added!")

@app.on_message(filters.command("list_anime_characters"))
async def list_anime_characters_handler(_, message: Message):
    characters_list = "\n".join([f"Name: {char['name']} | Rank: {char['rank']} | Anime: {char['anime']}" for char in anime_character_manager.anime_characters])
    response = f"List of anime characters:\n\n{characters_list}"
    await message.reply(response)

# ... (other code)

@app.on_message(filters.command("reset_harem") & filters.user(is_developer))
def reset_harem(bot, message: Message):
    user_id = int(message.text.split()[1])
    db_manager.reset_user_harem(user_id)
    
    bot.send_message(message.chat.id, f"Harem for user {user_id} reset successfully!")
