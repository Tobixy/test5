import random

class CharacterManager:
    def __init__(self):
        self.characters = [
            {"id": 1, "name": "Character A", "rank": "Common"},
            {"id": 2, "name": "Character B", "rank": "Rare"},
            {"id": 3, "name": "Character C", "rank": "Epic"},
            # ... add more characters here
        ]
        self.collected_characters = {}

    def spawn_random_character(self):
        return random.choice(self.characters)

    def collect_character(self, user_id, character):
        if user_id not in self.collected_characters:
            self.collected_characters[user_id] = []
        self.collected_characters[user_id].append(character)

    def get_user_collected_characters(self, user_id):
        return self.collected_characters.get(user_id, [])

character_manager = CharacterManager()
