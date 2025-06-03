import pygame
import uuid

class Card:
    def __init__(self, name, value, type, rarity, description, prize, damage=0):
        self._id = uuid.uuid4().hex  # Unique ID for each card
        self._name = name
        self._value = value
        self._type = type
        self._rarity = rarity
        self._description = description
        self._prize = prize
        self.damage = damage
        self.gameworld = None

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value
    
    @property
    def type(self):
        return self._type
