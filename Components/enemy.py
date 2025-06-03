import pygame
import time
import random
from Components.component import Component
from soundmanager import SoundManager


class Enemy(Component):
    def __init__(self, name, health, attack, strategy):
        super().__init__()
        self._name = name
        self._health = health
        self._attack = attack
        self._is_alive = True
        self._strategy = strategy
        self._max_health = health  # Store the maximum health for potential future use
        self.hit_timer = 0
        self.shake_offset = (0, 0)
        self.damage_popup = None
        self.damage_popup_timer = 0

    @property
    def name(self):
        return self._name

    @property
    def health(self):
        return self._health

    @property
    def attack(self):
        return self._attack
    
    @property
    def is_alive(self):
        return self._is_alive

    
    def take_damage(self, damage):
        if self._is_alive:
            self._health -= damage
            self.hit_timer = 0.15  # seconds to flash white and shake
            self.damage_popup = damage
            self.damage_popup_timer = 0.7  # seconds to show damage
            if self._health <= 0:
                self._is_alive = False
                print(f"{self._name} has been defeated!")
                self.gameObject.is_destroyed = True #remove enemy from game world
                SoundManager().play_sound("explosion")
                self.game_world.game_state = "map" # Transition to the map state
        else:
            print(f"{self._name} is already defeated.")

    def awake(self, game_world):
        self.game_world = game_world
    
    def start(self):
        pass

    def update(self, delta_time):
        # Handle shake and flash
        if self.hit_timer > 0:
            self.hit_timer -= delta_time
            self.shake_offset = (random.randint(-8, 8), random.randint(-8, 8))
        else:
            self.shake_offset = (0, 0)
        # Handle damage popup
        if self.damage_popup_timer > 0:
            self.damage_popup_timer -= delta_time
            if self.damage_popup_timer <= 0:
                self.damage_popup = None

    def enemy_action(self):
        self._strategy.choose_action(self._attack)

    def draw(self, screen, base_position, sprite_image):
        # Apply shake
        pos = (base_position[0] + self.shake_offset[0], base_position[1] + self.shake_offset[1])
        # Flash white if hit
        if self.hit_timer > 0:
            white_sprite = sprite_image.copy()
            white_sprite.fill((255,255,255), special_flags=pygame.BLEND_RGB_ADD)
            screen.blit(white_sprite, pos)
        else:
            screen.blit(sprite_image, pos)
        # Draw damage popup
        if self.damage_popup is not None:
            font = pygame.font.Font(None, 48)
            dmg_text = font.render(f"-{self.damage_popup}", True, (255, 0, 0))
            screen.blit(dmg_text, (pos[0] + 40, pos[1] - 40))