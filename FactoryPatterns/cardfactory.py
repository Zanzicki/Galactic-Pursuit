from Components.card import Card
from Components.component import SpriteRenderer, Transform
import random
from gameobject import GameObject
import pygame
from FactoryPatterns.factorypattern import Factory
from FactoryPatterns.artifactFactory import ArtifactFactory
from Components.cardHoverHandler import CardHoverHandler

class CardFactory(Factory):
    def create_component(self):
        go = GameObject(pygame.math.Vector2(250, 250))
        go.add_component(Card("Card", 0, "Card", "Common", "A simple card", 67))
        go.add_component(SpriteRenderer("Cards/floppycard.png"))
        go.add_component(CardHoverHandler())
        return go
    
    def create_component(self, card):
        go = GameObject(pygame.math.Vector2(250, 250))
        go.add_component(card)
        go.add_component(SpriteRenderer(("Cards/floppycard.png")))
        go.add_component(CardHoverHandler())
        go.get_component("SpriteRenderer").sprite_image = pygame.transform.scale(go.get_component("SpriteRenderer").sprite_image, (200, 200))
        return go