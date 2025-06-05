import random

import pygame
from Components.component import Component
from Components.player import Player
from StatePattern.statemachine import BossStateMachine
from StatePattern.boss_states import IdleState
from Components.hiteffect import HitEffect

class Boss(Component, HitEffect):
    def __init__(self, name: str, damage: int, health: int):
        Component.__init__(self)
        HitEffect.__init__(self)
        
        super().__init__()
        self._name = name
        self._health = health
        self._max_health = health
        self._damage = damage
        self._is_alive = True
        self.state_machine = BossStateMachine(self, None)  # Set player later
        self.hit_timer = 0
        self.shake_offset = (0, 0)
        self.damage_popup = None
        self.damage_popup_timer = 0

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
            self.trigger_hit(damage)
            if self._health <= 0:
                self._is_alive = False
                print(f"{self._name} has been defeated!")
                self.gameObject.is_destroyed = True #remove enemy from game world
                
                self.game_world._game_state = "end_game" # Transition to the map state
        else:
            print(f"{self._name} is already defeated.")

    def awake(self, game_world):
        self.game_world = game_world
        
    
    def start(self):
        pass

    def update(self, delta_time):
        if self.state_machine.player is None:
            self.state_machine.player = Player.get_instance()
        self.update_hit_effect(delta_time)
        animator = self.gameObject.get_component("Animator")
        if hasattr(self, "is_hit_animating") and self.is_hit_animating:
            if animator:
                animator.run_animation = False
        else:
            if animator:
                animator.run_animation = True

    def draw(self, screen, base_position, sprite_image):
        self.draw_hit_effect(screen, sprite_image, base_position)

    def defend(self):
        heal_amount = 10  # or whatever value
        self._health += heal_amount  # Allow overheal
        print(f"{self._name} heals for {heal_amount}! Current health: {self._health}")

    def enraged_attack(self, player):
        # Example: Stronger attack
        damage = self._damage * 2
        player.take_damage(damage)
        print(f"{self._name} deals {damage} enraged damage to the player!")

    def boss_action(self):
        if self.state_machine.current_state:
            self.state_machine.current_state.execute(self, self.state_machine.player)

    def get_state_icon(self):
        if self.state_machine.current_state is None:
            return None
        return getattr(self.state_machine.current_state, "icon_type", None)