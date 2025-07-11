import random
from StrategyPattern.strategy import Strategy
from Components.player import Player
from soundmanager import SoundManager


class TheBlueCentipedeStrategy(Strategy):
    def __init__(self,enemny_name):
        self._name = enemny_name
        self._actions = [self.basic_attack, self.basic_defense, self.special_skill]
        self._target = Player.get_instance()
        self.strength = None
        
    def choose_action(self, attack_value):
        self.strength = attack_value
        random_action = random.choice(self._actions)
        random_action()

    def basic_attack(self):
        self._target.take_damage(self.strength)
        print(f"{self._name} performs a basic attack for {self.strength} damage!")
        print(f"{self._target} has {self._target.health} health left.")
        SoundManager().play_sound("laser")
        

    def basic_defense(self):
        print(f"{self._name} performs a basic defense!")
        SoundManager().play_sound("shield_up")

    def special_skill(self):
        print(f"{self._name} uses a special skill!")