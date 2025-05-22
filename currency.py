import pygame
import State.shop as shop
credit_score = 0
scrap = 0

def addScrap():
    scrap+=10

def addCredits():
    credit_score += 15

def buyingWithScrap():
    if(scrap - shop.upgrade_cost>0):
        scrap-shop.upgrade_cost
    elif(scrap-shop.repair_cost>0):
        scrap-shop.repair_cost
    else:
        print("I do not have the required material.")
        
def buyingWithCredits():
    if(credit_score-shop.item_cost>0):
        credit_score-shop.item_cost
    else:
        print("I cannot afford that.")

def subtractScrap():
    scrap-=7

def subtractCredits():
    credit_score -=12
    