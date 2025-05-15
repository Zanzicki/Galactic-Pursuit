import random
from StrategyPattern.strategy import Strategy
from Components.player import Player


class ArangelStrategy(Strategy):
    def __init__(self,enemny_name):
        self._name = enemny_name
        self._actions = [self.basic_attack, self.basic_defense, self.special_skill]
        self._target = Player.get_instance()
        
    def choose_action(self):
        # random_action = random.choice(self._actions, target)
        # random_action()
        self.basic_attack()

    def basic_attack(self):
        self._target.take_damage(10)
        print(f"{self._name} performs a basic attack for 10 damage!")
        print(f"{self._target} has {self._target.health} health left.")

    def basic_defense(self):
        print(f"{self._name} performs a basic defense!")

    def special_skill(self):
        print(f"{self._name} uses a special skill!")