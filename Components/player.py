from gameobject import GameObject
import pygame
from Components.component import Component

class Player(Component):
    def __init__(self, deck, speed=5):
        super().__init__()
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
    
    def update(self, delta_time):
            # Handle ship movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.ship_pos[0] -= self.ship_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.ship_pos[0] += self.ship_speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.ship_pos[1] -= self.ship_speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.ship_pos[1] += self.ship_speed
