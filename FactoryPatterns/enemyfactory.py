from Components.component import SpriteRenderer, Transform
import random
from StrategyPattern.strategy import Strategy
from gameObject import GameObject
import pygame
from FactoryPatterns.factorypattern import Factory
from Components.enemy import Enemy
from StrategyPattern.arangelstrategy import ArangelStrategy

class EnemyFactory(Factory):
    def create_component(self, enemy_type):
        go = GameObject(pygame.math.Vector2(250, 250))
        if enemy_type == "Arangel":
            go.add_component(Enemy(enemy_type, 100, 20, ArangelStrategy(enemy_type)))
            go.add_component(SpriteRenderer("Enemies/Arangel.png"))
        elif enemy_type == "Gorpi":
            go.add_component(Enemy("Gorpi", 120, 25, Strategy(ArangelStrategy)))
            go.add_component(SpriteRenderer("Enemies/Gorpi.png"))
        elif enemy_type == "The Blue Centipede":
            go.add_component(Enemy("The Blue Centipede", 150, 30, Strategy(ArangelStrategy)))
            go.add_component(SpriteRenderer("Enemies/The Blue Centipede.png"))
        else:
            raise ValueError("Unknown enemy type")
        
        return go