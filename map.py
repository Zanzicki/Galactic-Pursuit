import pygame
import random
from Components.planet import Planet
from gameobject import GameObject

class Map:
    def __init__(self, game_world):
        self.game_world = game_world  # Reference to the GameWorld
        self.planets = []  # List to store all planets
        self.font = pygame.font.Font(None, 36)

    def generate_planets(self):
        colors = [
            (255, 0, 0),   # Red (Fight)
            (0, 255, 0),   # Green (Artifact)
            (0, 0, 255),   # Blue (Shop)
            (255, 0, 255), # Magenta (Mystery)
        ]
        planet_names = [
            "Mercury", "Venus", "Earth", "Mars", "Jupiter",
            "Saturn", "Uranus", "Neptune", "Pluto", "Eris"
        ]
        for i in range(10):  # Generate 10 planets
            name = planet_names[i]
            size = random.randint(35, 50)
            color = random.choice(colors)
            position = (
                random.randint(size + 10, self.game_world.width - size - 10),
                random.randint(size + 10, self.game_world.height - size - 10)
            )
            planet = GameObject(position)
            planet.add_component(Planet(name, size, color, position, self.game_world))
            self.planets.append(planet)  # Add planet to the list
            self.game_world._gameObjects.append(planet)  # Add planet to the game objects

    def draw(self, screen):
        for planet in self.planets:
            planet.draw(screen, self.font)