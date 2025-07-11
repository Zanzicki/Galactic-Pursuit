import pygame
from BuilderPattern.builder import Builder
from Components.component import SpriteRenderer
from Components.deck import Deck
from Components.player import Player
from gameobject import GameObject


class PlayerBuilder(Builder):
    def __init__(self):
        self.player = Player.get_instance()  # Always use the singleton

    def build(self):
        self._gameObject = GameObject(pygame.math.Vector2(250, 250))
        self._gameObject.add_component(self.player)
        self._gameObject.add_component(SpriteRenderer("Assets/spaceShip_01.png"))
        self._gameObject.get_component("SpriteRenderer").sprite_image = pygame.transform.scale(self._gameObject.get_component("SpriteRenderer").sprite_image, (50, 50))
        self._gameObject.transform.position = [800 // 2, 600 // 2]  # Center the ship
        self.player.deck = Deck()  # Set the deck for the player

    def get_gameObject(self) -> GameObject:
        return self._gameObject