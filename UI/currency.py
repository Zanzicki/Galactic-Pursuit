import pygame
from Components.player import Player
from GameState.shop import Shop
from Database.sqlrepository import SQLRepository

class Currency:
    def __init__(self):
        self.player = Player.get_instance()
        self.shop = Shop._instance
        self.repository = SQLRepository()

    @staticmethod
    def get_instance(player):
        if not hasattr(Currency, "_instance"):
            Currency._instance = Currency(player)
        return Currency._instance

    def addCredit(self, credit_amount):
        self.player._credits += credit_amount
        print(f"Credit score increased to {self.player._credits}.")
        self.repository.update_player_currency(self.player._id, credits=self.player._credits)
        self.player._credits += credit_amount  # Ensure the player's credit score is updated

    def addScrap(self, scrap_amount):
        self.player._scraps += scrap_amount
        print(f"Scrap increased to {self.player._scraps}.")
        self.repository.update_player_currency(self.player._id, scrap=self.player._scraps)
        self.player._scraps += scrap_amount  # Ensure the player's scrap score is updated

    def buyingWithScrap(self):
        if self.player._scraps - self.shop.item_cost > 0:
            self.player._scraps -= self.shop.item_cost
            self.repository.update_player_currency(self.player._id, scrap=self.player._scraps)
        else:
            print("I cannot afford that.")

    def buyingWithCredits(self):
        if self.player._credits - self.shop.item_cost > 0:
            self.player._credits -= self.shop.item_cost
            self.repository.update_player_currency(self.player._id, credits=self.player._credits)
        else:
            print("I cannot afford that.")


