import pygame
from BuilderPattern.builder import Builder
from Components.component import SpriteRenderer
from Components.deck import Deck
from Components.player import Player
from gameobject import GameObject


class PlayerBuilder(Builder):

    def build(self):
        self._gameObject = GameObject(pygame.math.Vector2(250, 250))
        self._gameObject.add_component(Deck())
        self._gameObject.add_component(Player())
        self._gameObject.add_component(SpriteRenderer("asssets/spaceShip_01.png"))
        return self.player