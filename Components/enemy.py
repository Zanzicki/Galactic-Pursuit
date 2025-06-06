import pygame
import time
import random
from Components.component import Component
from Components.hiteffect import HitEffect
from GameState.rewardscreen import RewardScreen
from soundmanager import SoundManager


class Enemy(Component, HitEffect):
    def __init__(self, name, health, attack, strategy):
        super().__init__()
        Component.__init__(self)
        HitEffect.__init__(self)
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
        self._health -= damage
        self.trigger_hit(damage)
        if self._health <= 0:
            self._is_alive = False
            print(f"{self._name} has been defeated!")
            self.gameObject.is_destroyed = True #remove enemy from game world
            SoundManager().play_sound("explosion")
            self._game_world.game_state = "reward_screen"
            self.reward_screen = RewardScreen(self._game_world)
        else:
            print(f"{self._name} is already defeated.")

    def awake(self, game_world):
        self.game_world = game_world
    
    def start(self):
        pass

    def update(self, delta_time):
        self.update_hit_effect(delta_time)

    def enemy_action(self):
        self._strategy.choose_action(self._attack)

    def draw(self, screen, base_position, sprite_image):
         self.draw_hit_effect(screen, sprite_image, base_position)