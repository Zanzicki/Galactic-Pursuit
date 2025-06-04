import pygame
from BuilderPattern.builder import Builder
from Components.component import SpriteRenderer
from gameobject import GameObject
from Components.boss import Boss  # Assuming Boss is defined in Components/boss.py


class BossBuilder(Builder):
    def __init__(self):
        self.boss = Boss()  # Assuming Boss is a class that needs to be defined or imported
        self.spritesheet = []  # List to hold sprites for the boss

    def build(self):
        self._gameObject = GameObject(pygame.math.Vector2(250, 250))
        self._gameObject.add_component(self.boss)
        self._gameObject.add_component(SpriteRenderer("07bc194f-6de5-4f8c-9f4d-2940f07bd283-0.png"))  # Path to the boss sprite
        self._gameObject.get_component("SpriteRenderer").sprite_image = pygame.transform.scale(self._gameObject.get_component("SpriteRenderer").sprite_image, (50, 50))
        for sprite in "Assets\\Enemies\\Boss":
            self.spritesheet.append(sprite) 
            self._gameObject.get_component("SpriteRenderer").sprite_image = pygame.image.load(sprie)
        self._gameObject.get_component("SpriteRenderer").add_animation("idle", [self.spritesheet])  
        self._gameObject.transform.position = [800 // 2, 600 // 2]  # Center the ship
        
    
    def get_gameObject(self) -> GameObject:
        return self._gameObject