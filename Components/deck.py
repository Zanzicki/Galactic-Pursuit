import random
from Database.sqlrepository import SQLRepository
from Components.card import Card
from FactoryPatterns.cardfactory import CardFactory

class Deck:
    def __init__(self):
        self.repository = SQLRepository()
        self.draw_pile = []
        self.discarded_cards = []
        self.hand = []
        self.decklist = []        
        self.cardfactory = CardFactory()
        self.card_positions = []

    def add_card(self, card: Card):
        self.decklist.append(card)
        print (f"Card added: {card.name} (ID: {card._id})")

    def remove_card(self, card: Card):
        if card in self.decklist:
            self.decklist.remove(card)

    def shuffle_draw_pile(self):
        random.shuffle(self.draw_pile)

    def initialize_draw_pile(self):
        self.draw_pile = list(self.decklist)
        self.discarded_cards.clear()
        self.hand.clear()
        self.shuffle_draw_pile()
        print("After initialize_draw_pile:")

    def draw_card(self):
        if not self.draw_pile:
            if self.discarded_cards:
                self.draw_pile = self.discarded_cards[:]
                random.shuffle(self.draw_pile)
                self.discarded_cards.clear()
            else:
                return None
        card = self.draw_pile.pop()
        self.hand.append(card)
        return card

    def draw_hand(self, hand_size=5):
        self.hand.clear()
        for _ in range(hand_size):
            card = self.draw_card()
            if card is None:
                break

    def play_card(self, card):
        # Remove by id, not by object identity
        for hand_card in self.hand:
            if getattr(hand_card, "_id", None) == getattr(card, "_id", None):
                self.hand.remove(hand_card)
                self.discarded_cards.append(hand_card)
                break

    def discard_hand(self):
        self.discarded_cards.extend(self.hand)
        self.hand.clear()

    def create_starter_deck(self):
        cardfromdb = self.repository.fetch_basic_cards() 
        if not cardfromdb:
            raise ValueError("No cards found in the database.")
        for card_data in cardfromdb:
            if card_data[0] == 1 or card_data[0] == 2:
                for i in range(4):
                    name, value, type, rarity, description, prize = card_data[1], card_data[2], card_data[3], card_data[4], card_data[5], card_data[6]
                    card = Card(name, value, type, rarity, description, prize)
                    self.add_card(card)

    # In Deck.__init__ or dynamically in draw_cards
    def get_card_positions(self, screen_width, y=500, card_count=5, card_width=150, spacing=40):
        total_width = card_count * card_width + (card_count - 1) * spacing
        start_x = (screen_width - total_width) // 2
        return [(start_x + i * (card_width + spacing), y) for i in range(card_count)]
