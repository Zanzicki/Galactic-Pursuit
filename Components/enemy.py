from Components.component import Component
import random

class Enemy(Component):
    def __init__(self, name, health, attack, actions):
        super().__init__()
        self._name = name
        self._health = health
        self._attack = attack
        self._actions = actions
        self._is_alive = True

    @property
    def name(self):
        return self._name

    @property
    def health(self):
        return self._health

    @property
    def attack(self):
        return self._attack
    
    def enemy_action(self):
        random_action = random.choice(self._actions)
        if random_action == "attack":
            print(f"{self._name} attacks!")
        elif random_action == "defend":
            print(f"{self._name} defends!")
        elif random_action == "skill":
            print(f"{self._name} uses a skill!")