from Components.card import Card
from FactoryPatterns.factory import Factory

class CardFactory(Factory):
    def create_component(self, name, value, type, rarity, description, image_path):
        return Card(name, value, type, rarity, description, image_path)