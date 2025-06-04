from Components.component import SpriteRenderer, Transform
import random
from StrategyPattern.strategy import Strategy
from gameobject import GameObject
import pygame
from FactoryPatterns.factorypattern import Factory
from Components.enemy import Enemy
from StrategyPattern.arangelstrategy import ArangelStrategy
from StrategyPattern.gorpistrategy import GorpiStrategy
from StrategyPattern.thebluecentipedestrategy import TheBlueCentipedeStrategy
from soundmanager import SoundManager

class EnemyFactory(Factory):
    def create_component(self, enemy_type):
        go = GameObject(pygame.math.Vector2(250, 250))
        if enemy_type == "Arangel":
            go.add_component(Enemy(enemy_type, 100, 20, ArangelStrategy(enemy_type)))
            go.add_component(SpriteRenderer("Assets/Enemies/Arangel.png"))
            SoundManager().play_sound("alienspawn")
        elif enemy_type == "Gorpi":
            go.add_component(Enemy(enemy_type, 120, 25, GorpiStrategy(enemy_type)))
            go.add_component(SpriteRenderer("Assets/Enemies/Gorpi.png"))
            SoundManager().play_sound("alienspawn")
        elif enemy_type == "The Blue Centipede":
            go.add_component(Enemy(enemy_type, 150, 30, TheBlueCentipedeStrategy(enemy_type)))
            go.add_component(SpriteRenderer("Assets/Enemies/The Blue Centipede.png"))
            SoundManager().play_sound("alienspawn")
        else:
            raise ValueError("Unknown enemy type")
        
        return go