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
    
    @property
    def take_damage(self):
        raise AttributeError("This property is write-only.")

    
    def take_damage(self, damage):
        if self._is_alive:
            self._health -= damage
            if self._health <= 0:
                self._is_alive = False
                print(f"{self._name} has been defeated!")
                self.gameObject.is_destroyed = True #remove enemy from game world
                
                self.game_world.state = "map" # Transition to the map state
        else:
            print(f"{self._name} is already defeated.")

    def awake(self, game_world):
        self.game_world = game_world
    
    def start(self):
        pass

    def update(self, delta_time):
        pass
    
    def enemy_action(self):
        self._strategy.choose_action(self._attack)