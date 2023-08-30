import os
from pymongo import MongoClient

MONGO_URL = ("MONGO_URL")  # Retrieve MongoDB URI from Heroku environment variables
DB_NAME = "anime_characters"

class DatabaseManager:
    def __init__(self):
        self.client = MongoClient(MONGO_URL)
        self.db = self.client[DB_NAME]

    def insert_character(self, character_info):
        self.db.characters.insert_one(character_info)

    def get_character_by_name(self, character_name):
        return self.db.characters.find_one({"name": character_name})

    def reset_user_harem(self, user_id):
        self.db.harems.update_one({"user_id": user_id}, {"$set": {"characters": []}}, upsert=True)

    def get_shared_harem(self):
        return self.db.harems.find_one({"user_id": "shared"}).get("characters", [])

    # Add more methods as needed

database_manager = DatabaseManager()
