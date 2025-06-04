import pygame
from Database.sqlrepository import SQLRepository
from Components.component import Component
from Database.database import Database
from soundmanager import SoundManager


class Player(Component):
    _instance = None  # Class-level attribute to store the single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Player, cls).__new__(cls)
        return cls._instance

    def __init__(self, health=100, speed=300, id=None, credits=0, scraps=0, max_health=100):
        if not hasattr(self, "_initialized"):  # Ensure __init__ is only called once
            super().__init__()
            self._speed = speed
            self._health = health
            self.game_world = None  # Reference to the GameWorld
            self.events = None
            self._initialized = True  # Mark as initialized
            self.deck = None
            self.block_points = 0 
            self.repository = SQLRepository()
            self._id = id
            self._credits = credits
            self._scraps = scraps
            self._max_health = max_health
            self.artifacts = []
            self.artifact_positions = []
            self.temp_health = 0

    @staticmethod
    def get_instance():
        if Player._instance is None:
            Player._instance = Player()
        return Player._instance

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        if value > self._max_health:
            self._health = self._max_health
        else:
            self._health = value
        self.update_db()
    
    @property
    def credits(self):
        return self._credits
    
    @credits.setter
    def credits(self, value):
        self._credits = value
        self.update_db()

    @property
    def scraps(self):
        return self._scraps
    
    @scraps.setter
    def scraps(self, value):
        self._scraps = value
        self.update_db()

    def add_temp_health(self, amount):
        self.temp_health += amount

    def take_damage(self, damage):

        if self.block_points > 0:
            print("BLOCKING damage!")
            self.block_points -= 1
            print(f"Block points left: {self.block_points}")
            return
        
        if self.temp_health > 0:
            if damage <= self.temp_health:
                self.temp_health -= damage
                damage = 0
            else:
                damage -= self.temp_health
                self.temp_health = 0
        if damage > 0:
            self._health -= damage
            if self._health <= 0:
                self._gameObject.is_destroyed = True
                print(f"{self._gameObject} has been defeated!")
                SoundManager().play_sound("explosion")
        else:
            print(f"{self._gameObject} is already defeated.")

    def awake(self, game_world):
        self.game_world = game_world  # Store reference to the GameWorld

    def start(self):
        pass

    def update(self, delta_time):
        # Handle ship movement
        keys = pygame.key.get_pressed()
        movement = pygame.math.Vector2(0, 0)

        # Movement controls
        if keys[pygame.K_a]:
            movement.x -= self._speed  # Move left
        if keys[pygame.K_d]:
            movement.x += self._speed  # Move right
        if keys[pygame.K_w]:
            movement.y -= self._speed  # Move up
        if keys[pygame.K_s]:
            movement.y += self._speed  # Move down

        # Apply movement
        self._gameObject.transform.translate(movement * delta_time)

    def update_artifacts(self):
        self.artifact_positions.clear()
        self.artifact_positions = [(20 + i * 40, 60) for i in range(len(self.artifacts))]

        # Update artifact positions based on the current artifacts
        for index, artifact in enumerate(self.artifacts):
            artifact.transform.position = self.artifact_positions[index]
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self._gameObject.transform.position.x - 10,
                                                   self._gameObject.transform.position.y - 10, 20, 20))

    def get_events(self, events):
        self.events = events

    def update_db(self):
        player_id = self.repository.fetch_player_id(self.name)
        self.repository.update_player_currency(player_id, credits=self.credits, scrap=self.scraps, health=self.health, max_health=self._max_health)