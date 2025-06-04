import os
import pygame
from BuilderPattern.builder import Builder
from Components.component import Animator, SpriteRenderer
from gameobject import GameObject
from Components.boss import Boss


class BossBuilder(Builder):
    def __init__(self, name: str, damage: int, max_health: int):
        self.boss = Boss(name, damage, max_health)
        self.spritesheet = []

    def build(self):
        self._gameObject = GameObject(pygame.math.Vector2(250, 250))
        self._gameObject.add_component(self.boss)
        boss_folder = "Assets/Enemies/Boss"
        # List all files in the boss folder and add full paths to spritesheet
        self.spritesheet = [
            os.path.join(boss_folder, f)
            for f in os.listdir(boss_folder)
            if f.lower().endswith(('.png'))
        ]
        # Optionally sort for consistent animation order
        self.spritesheet.sort()
        # Use the first sprite as the default
        if self.spritesheet:
            self._gameObject.add_component(SpriteRenderer(self.spritesheet[0]))
            # self._gameObject.get_component("SpriteRenderer").sprite_image.convert_alpha()

        self._gameObject.add_component(Animator())
        self._gameObject.get_component("Animator").add_animation("idle", *self.spritesheet)
        self._gameObject.get_component("Animator").play_animation("idle")
    def get_gameObject(self) -> GameObject:
        return self._gameObject