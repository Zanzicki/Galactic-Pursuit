from Components.card import Card
from database import Database
from FactoryPatterns.cardfactory import CardFactory

class Deck:
    def __init__(self):
        self.full_deck = []
        self.discarded_cards = []
        self.draw_pile = []
        self.hand = []
        self.db = Database()
        self.create_starter_deck()
        self.cardlist = []        
        self.cardfactory = CardFactory()
        self.card_positions = [(100,500), (300,500), (500,500), (700,500), (900,500)]
    
    @property
    def cardsindeck(self):
        return self.full_deck
    
    @property
    def discarded_cards(self):
        return self._discarded_cards
    
    @discarded_cards.setter
    def discarded_cards(self, value):
        if isinstance(value, list):
            self._discarded_cards = value
        else:
            raise ValueError("discarded_cards must be a list")
        
    @property
    def draw_pile(self):
        return self._draw_pile
    
    @draw_pile.setter
    def draw_pile(self, value):
        if isinstance(value, list):
            self._draw_pile = value
        else:
            raise ValueError("draw_pile must be a list")

    def add_card(self, card: Card):
        self.full_deck.append(card)

    def remove_card(self, card: Card):
        if card in self.full_deck:
            self.full_deck.remove(card)

    def shuffle(self):
        import random
        random.shuffle(self.full_deck)

    def draw_card(self):
        if self.full_deck:
            return self.full_deck.pop(0)  # Remove and return the top card
        return None  # Return None if the deck is empty

    def __len__(self):
        return len(self.full_deck)
    
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
    
    def discard_hand(self):
        self.discarded_cards.extend(self.hand)
        self.hand.clear()

    def draw_hand(self, hand_size=5):
        # If deck is empty, reshuffle discard into deck
        if len(self.full_deck) < hand_size:
            self.full_deck.extend(self.discarded_cards)
            self.discarded_cards.clear()
            self.shuffle()
        self.hand = []
        for _ in range(hand_size):
            card = self.draw_card()
            if card:
                self.hand.append(card)
        return self.hand
