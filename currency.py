import pygame
from Components.player import Player
from State.shop import Shop
from database import Database

class Currency:
    def __init__(self, player):
        self.player = player  
        self.shop = Shop.get_instance()
        self.db = Database()
        self.credits = 0
        self.scrap = 0

    @staticmethod
    def get_instance(player):
        if not hasattr(Currency, "_instance"):
            Currency._instance = Currency(player)
        return Currency._instance

    def addCredit(self, credit_amount):
        self.credits += credit_amount
        print(f"Credit score increased to {self.credits}.")
        self.db.update_player_currency(self.player.id, credits=self.credits)  # Updateself.db

    def addScrap(self, scrap_amount):
        self.scrap += scrap_amount
        print(f"Scrap increased to {self.scrap}.")
        self.db.update_player_currency(self.player.id, scrap=self.scrap)  # Updateself.db

    def buyingWithScrap(self):
        if self.scrap - self.shop.item_cost > 0:
            self.scrap -= self.shop.item_cost
            self.db.update_player_currency(self.player.id, scrap=self.scrap)
        else:
            print("I cannot afford that.")

    def buyingWithCredits(self):
        if self.credits - self.shop.item_cost > 0:
            self.credits -= self.shop.item_cost
            self.db.update_player_currency(self.player.id, credits=self.credits)
        else:
            print("I cannot afford that.")


