import pygame
from Components.player import Player
import State.shop as shop
class Currency:
    def __init__(self):
        self.credit_score = 0
        self.scrap = 0

    @staticmethod
    def get_instance():
        if not hasattr(Currency, "_instance"):
            Currency._instance = Currency()
        return Currency._instance
    
    def addCredit(self, credit_amount):
        self.credit_score += credit_amount
        print(f"Credit score increased to {self.credit_score}.")

    def addScrap(self, scrap_amount):
        self.scrap += scrap_amount
        print(f"Scrap increased to {self.scrap}.")

    def buyingWithScrap():
        if(scrap-shop.item_cost>0):
            scrap -= shop.item_cost
        else:
            print("I cannot afford that.")
            
    def buyingWithCredits():
        if(credit_score-shop.item_cost>0):
            credit_score -= shop.item_cost
        else:
            print("I cannot afford that.")


        