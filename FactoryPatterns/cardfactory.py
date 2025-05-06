from Components.card import Card
from FactoryPatterns.factory import Factory
import random

class CardFactory(Factory):
    def create_component(self):
        r = random.randint(1, 13)
        if r < 10:
            r = "0" + str(r)           
        file_path = f"Assets\\Club_card_{r}.png"
        return Card(name = "test card", value = 1, type = "common", rarity = "common", description = "test card", image_path = file_path)