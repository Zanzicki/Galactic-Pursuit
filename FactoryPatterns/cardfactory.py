from Components.card import Card
from Components.component import SpriteRenderer, Transform
import random
from gameobject import GameObject
import pygame
from FactoryPatterns.factorypattern import Factory
from FactoryPatterns.artifactFactory import ArtifactFactory

class CardFactory(Factory):
    def create_component(self):
        go = GameObject(pygame.math.Vector2(250, 250))
        go.add_component(Card("Card", 0, "Card", "Common", "A simple card", 67))
        r = random.randint(1, 13)
        if r < 10:
            r = "0" + str(r)           
        file_path = f"Cards/Clubs_card_{r}.png"
        go.add_component(SpriteRenderer(file_path))
        return go
    
    def create_component(self, card):
        go = GameObject(pygame.math.Vector2(250, 250))
        go.add_component(card)
        r = random.randint(1, 13)
        if r < 10:
            r = "0" + str(r)           
        file_path = f"Cards/Clubs_card_{r}.png"
        go.add_component(SpriteRenderer(file_path))
        return go
