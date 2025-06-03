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

    def take_damage(self, damage):
        

        if self.block_points > 0:
            print("BLOCKING damage!")
            self.block_points -= 1
            print(f"Block points left: {self.block_points}")
            return
        
        if self._health > 0:
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

        # Check for interaction with planets when spacebar is pressed
        for event in self.events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.check_planet_interaction()

    def check_planet_interaction(self):
        print("Checking planet interaction...")
        player_position = self._gameObject.transform.position

        # Access planets from the Map class
        planets = self.game_world.map.planets

        for planet in planets:
            dx = player_position.x - planet.transform.position[0]
            dy = player_position.y - planet.transform.position[1]
            planetcomponent = planet.get_component("Planet")
            
            if planetcomponent._visited:
             continue
            
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance <= planetcomponent._size + 20:  # Check if the player is close enough to the planet
                planetcomponent._visited = True  # Mark the planet as visited
                self.game_world.map.check_and_spawn_boss()
                self.repository.change_planet_explored(self._id, planetcomponent._name)
                
                  # Check if the boss should spawn
                if planetcomponent._name == "Boss":
                    print("Boss planet reached!")
                    self.game_world._game_state = "end_game"  # Transition to end game state
                    return
                if planetcomponent._color == (0, 0, 255):  # Blue (Shop)
                    print(f"{planetcomponent._name} (Blue): Entering shop!")
                    self.game_world.state_changed_to_shop = "into"
                    self.game_world._game_state= "shop"  # Transition to shop state
                    return
                elif planetcomponent._color == (255, 0, 0):  # Red (Fight)
                    print(f"{planetcomponent._name} (Red): Entering fight!")
                    self.game_world._game_state = "game"  # Transition to game state
                    return
                elif planetcomponent._color == (0, 255, 0):  # Green (Artifact)
                    print(f"{planetcomponent._name} (Green): Entering artifact!")
                    self.game_world._game_state = "artifact"
                elif planetcomponent._color == (255, 0, 255):
                    print(f"{planetcomponent._name} (Magenta): Entering mystery!")
                    self.game_world._game_state = "mystery"

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