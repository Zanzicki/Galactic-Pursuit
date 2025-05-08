import pygame
import pygame_gui
from array import array
import random
import currency
import upgrades
from Components import artifact
from Components import card

screen_width = 1080
screen_height = 720

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Interstellar Trade Sector")

item_cost = 25
upgrade_cost = 20
repair_cost = 8

available_upgrades = []
available_upgrades.append(upgrades.selected_dictionaries)

running = True
while running:
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False