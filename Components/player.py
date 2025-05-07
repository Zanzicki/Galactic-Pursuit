from gameObject import GameObject
import pygame
from Components.component import Component

class Player(Component):
    def __init__(self, position, deck, speed=5):
        super().__init__()
        self._position = position
        self._speed = speed
        self._deck = deck

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    def move(self, direction):
        self._position += direction * self._speed
    