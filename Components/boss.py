from Components.component import Component

class Boss(Component):
    def __init__(self, name: str, health: int, damage: int):
        super().__init__("Boss")
        self._name = name
        self._health = health
        self._damage = damage
        self._is_alive = True
        self._state = "neutral"

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
    
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, new_state):
        if new_state in ["neutral", "aggressive", "defensive"]:
            self._state = new_state
        else:
            raise ValueError("Invalid state. Must be 'neutral', 'aggressive', or 'defensive'.")

    
    def take_damage(self, damage):
        if self._is_alive:
            self._health -= damage
            if self._health <= 0:
                self._is_alive = False
                print(f"{self._name} has been defeated!")
                self.gameObject.is_destroyed = True #remove enemy from game world
                
                self.game_world.state = "end_game" # Transition to the map state
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