from gameobject import GameObject
import pygame
from Components.component import Component


class Player(Component):
    def __init__(self, deck, speed=500):
        super().__init__()
        self._speed = speed
        self._deck = deck
        self.game_world = None  # Reference to the GameWorld

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
        for event in pygame.event.get():
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
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance <= planetcomponent._size + 20:  # Check if the player is close enough to the planet
                if planetcomponent._color == (0, 0, 255):  # Blue (Shop)
                    print(f"{planetcomponent._name} (Blue): Entering shop!")
                    self.game_world._state = "shop"  # Transition to shop state
                    return
                elif planetcomponent._color == (255, 0, 0):  # Red (Fight)
                    print(f"{planetcomponent._name} (Red): Entering fight!")
                    self.game_world._state = "game"  # Transition to game state
                    return

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self._gameObject.transform.position.x - 10,
                                                   self._gameObject.transform.position.y - 10, 20, 20))
