from gameobject import GameObject
import pygame
from Components.component import Component

class Player(Component):
    def __init__(self, deck, speed=500):
        super().__init__()
        self._speed = speed
        self._deck = deck
    
    def awake(self, game_world):
         pass
    
    def start(self):
         pass
         
    
    def update(self, delta_time):
         # Handle ship movement
        keys = pygame.key.get_pressed()
        movement = pygame.math.Vector2(0, 0)

        # Movement controls
        if keys[pygame.K_a]:
            movement.x -= self._speed  # Move left
        if keys[pygame.K_d]:
            movement.x += self._speed  # Move left
        if keys[pygame.K_w]:
            movement.y -= self._speed
        if keys[pygame.K_s]:
            movement.y += self._speed

        self._gameObject.transform.translate(movement * delta_time)
