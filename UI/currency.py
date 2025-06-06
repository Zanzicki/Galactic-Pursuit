import pygame
from Components.player import Player
from GameState.shop import Shop
from Database.sqlrepository import SQLRepository

class Currency:
    def __init__(self):
        self.player = Player.get_instance()
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
        self.player._credits += credit_amount

    def addScrap(self, scrap_amount):
        self.player._scraps += scrap_amount
        print(f"Scrap increased to {self.player._scraps}.")
        self.repository.update_player_currency(self.player._id, scrap=self.player._scraps)
        self.player._scraps += scrap_amount


