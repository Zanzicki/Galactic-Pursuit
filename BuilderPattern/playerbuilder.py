import pygame
from BuilderPattern.builder import Builder
from Components.component import SpriteRenderer
from Components.deck import Deck
from Components.player import Player
from gameobject import GameObject


class PlayerBuilder(Builder):

    def build(self):
        self._gameObject = GameObject(pygame.math.Vector2(250, 250))
        deck = self._gameObject.add_component(Deck())
        self._gameObject.add_component(Player(deck))
        self._gameObject.add_component(SpriteRenderer("spaceShip_01.png"))
    
    def get_gameObject(self) -> GameObject:
        return self._gameObject