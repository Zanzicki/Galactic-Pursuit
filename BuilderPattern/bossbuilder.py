import pygame
from BuilderPattern.builder import Builder
from Components.component import SpriteRenderer
from gameobject import GameObject
from Components.boss import Boss  # Assuming Boss is defined in Components/boss.py


class BossBuilder(Builder):
    def __init__(self):
        self.boss = Boss()  # Assuming Boss is a class that needs to be defined or imported

    def build(self):
        self._gameObject = GameObject(pygame.math.Vector2(250, 250))
        self._gameObject.add_component(self.boss)
        self._gameObject.add_component(SpriteRenderer("spaceShip_01.png"))
        self._gameObject.get_component("SpriteRenderer").sprite_image = pygame.transform.scale(self._gameObject.get_component("SpriteRenderer").sprite_image, (50, 50))
        self._gameObject.transform.position = [800 // 2, 600 // 2]  # Center the ship
        
    
    def get_gameObject(self) -> GameObject:
        return self._gameObject