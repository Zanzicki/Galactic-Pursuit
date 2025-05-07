from Components.card import Card
from database import Database

class Deck:
    def __init__(self):
        self.cards = []
        self.db = Database()
        self.create_starter_deck()
    
    @property
    def cardsindeck(self):
        return self._cards

    def add_card(self, card: Card):
        self.cards.append(card)

    def remove_card(self, card: Card):
        if card in self.cards:
            self.cards.remove(card)

    def shuffle(self):
        import random
        random.shuffle(self.cards)

    def draw_card(self):
        if self.cards:
            return self.cards.pop(0)  # Remove and return the top card
        return None  # Return None if the deck is empty

    def __len__(self):
        return len(self.cards)
    
    def create_starter_deck(self):
        cardfromdb = self.db.fetch_basic_cards() 
        if not cardfromdb:
            raise ValueError("No cards found in the database.")
        
        for card_data in cardfromdb:  # Rename to card_data to avoid confusion
            print(card_data[0])
            if card_data[0] == 1 or card_data[0] == 2:
                for i in range(4):
                    name, value, type, rarity, description, prize = card_data[1], card_data[2], card_data[3], card_data[4], card_data[5], card_data[6]
                    card = Card(name, value, type, rarity, description, prize)
                    self.add_card(card)
                    print(f"Card {name} added to the deck")

            else:
                name, value, type, rarity, description, prize = card_data[1], card_data[2], card_data[3], card_data[4], card_data[5], card_data[6]
                card = Card(name, value, type, rarity, description, prize)
                self.add_card(card)
