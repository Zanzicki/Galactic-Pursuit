from Components.component import Component
from StatePattern.statemachine import BossStateMachine
from StatePattern.boss_states import IdleState

class Boss(Component):
    def __init__(self, name: str, damage: int, max_health: int):
        super().__init__()
        self._name = name
        self._health = max_health
        self._max_health = max_health
        self._damage = damage
        self._is_alive = True
        self.state_machine = BossStateMachine(self, None)  # Set player later

        # Initialize the boss in the Idle state
        self.state_machine.change_state(IdleState())

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

    def can_attack(self, player):
        # Your logic here
        return True

    def attack(self, player):
        # Your attack logic here
        player.take_damage(10)

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

    def update(self, delta_time, player):
        if self.state_machine.player is None:
            self.state_machine.player = player
        self.state_machine.update()

    def defend(self):
        # Example: Heal or gain block
        heal_amount = 10
        self._health = min(self._health + heal_amount, self._max_health)
        print(f"{self._name} heals for {heal_amount}! Current health: {self._health}")

    def enraged_attack(self, player):
        # Example: Stronger attack
        damage = self._damage * 2
        player.take_damage(damage)
        print(f"{self._name} deals {damage} enraged damage to the player!")