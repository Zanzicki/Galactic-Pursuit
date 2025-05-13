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
                print ("Spacebar pressed!")
                self.check_planet_interaction()

    def check_planet_interaction(self):
        player_position = self._gameObject.transform.position

        # Access planets from the Map class
        planets = self.game_world.map.planets

        for planet in planets:
            dx = player_position.x - planet._position[0]
            dy = player_position.y - planet._position[1]
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance <= planet._size + 20:  # Check if the player is close enough to the planet
                if planet._color == (0, 0, 255):  # Blue (Shop)
                    print(f"{planet._name} (Blue): Entering shop!")
                    self.game_world._state = "shop"  # Transition to shop state
                    return
                elif planet._color == (255, 0, 0):  # Red (Fight)
                    print(f"{planet._name} (Red): Entering fight!")
                    self.game_world._state = "game"  # Transition to game state
                    return
                elif planet._color == (0, 255, 0):  # Green (Artifact)
                    print(f"{planet._name} (Green): Entering artifact!")
                    self.game_world._state = "artifact"  # Transition to artifact state
                    return
                elif planet._color == (255, 0, 255):  # Magenta (Mystery)
                    print(f"{planet._name} (Magenta): Entering mystery!")
                    self.game_world._state = "mystery"  # Transition to mystery state
                    return
