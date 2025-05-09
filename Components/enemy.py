from Components.component import Component

class Enemy(Component):
    def __init__(self, name, health, attack, strategy):
        super().__init__()
        self._name = name
        self._health = health
        self._attack = attack
        self._is_alive = True
        self._strategy = strategy

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

    @is_alive.setter
    def is_alive(self, health):
        if health <= 0:
            self._is_alive = False
        else:
            self._is_alive = True
    
    def enemy_action(self, strategy):
        strategy.choose_action()