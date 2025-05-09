import random
from strategy import Strategy


class ArangelStrategy(Strategy):
    def choose_action(self):
        random_action = random.choice(self._actions)
        if random_action == "attack":
            print(f"{self._name} attacks!")
        elif random_action == "defend":
            print(f"{self._name} defends!")
        elif random_action == "skill":
            print(f"{self._name} uses a skill!")