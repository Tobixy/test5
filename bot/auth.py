from pyrogram.types import User
from main import app

AUTHORIZED_USERS = []

def is_developer(user: User) -> bool:
    return user.id in AUTHORIZED_USERS

def is_authorized(func):
    async def check_is_authorized(_, message):
        if message.from_user.id in AUTHORIZED_USERS:
            return await func(_, message)
        else:
            await message.reply("You are not authorized to use this command.")
    return check_is_authorized

@app.on_message(filters.command("add_developer"))
async def add_developer(_, message):
    if is_developer(message.from_user):
        if len(message.command) != 2:
            await message.reply("Please provide the user's ID to add as a developer.")
            return
        try:
            user_id = int(message.command[1])
            if user_id not in AUTHORIZED_USERS:
                AUTHORIZED_USERS.append(user_id)
                await message.reply("User added as a developer!")
            else:
                await message.reply("User is already a developer.")
        except ValueError:
            await message.reply("Invalid user ID.")

@app.on_message(filters.command("remove_developer"))
async def remove_developer(_, message):
    if is_developer(message.from_user):
        if len(message.command) != 2:
            await message.reply("Please provide the user's ID to remove from developers.")
            return
        try:
            user_id = int(message.command[1])
            if user_id in AUTHORIZED_USERS:
                AUTHORIZED_USERS.remove(user_id)
                await message.reply("User removed from developers!")
            else:
                await message.reply("User is not a developer.")
        except ValueError:
            await message.reply("Invalid user ID.")

# ... (rest of the code)
