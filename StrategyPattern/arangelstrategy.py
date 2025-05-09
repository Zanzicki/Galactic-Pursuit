import random
from StrategyPattern.strategy import Strategy


class ArangelStrategy(Strategy):
    def __init__(self,enemny_name):
        self._name = enemny_name
        self._actions = [self.basic_attack, self.basic_defense, self.special_skill]
        
    def choose_action(self):
        random_action = random.choice(self._actions)
        random_action()

    def basic_attack(self):
        print(f"{self._name} performs a basic attack!")

    def basic_defense(self):
        print(f"{self._name} performs a basic defense!")

    def special_skill(self):
        print(f"{self._name} uses a special skill!")