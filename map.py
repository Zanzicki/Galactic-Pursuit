import pygame
import random
import pygame_gui
from Components.planet import Planet
from gameobject import GameObject

class Map:
    def __init__(self, game_world):
        self.game_world = game_world  # Reference to the GameWorld
        self.planets = []  # List to store all planets
        self.font = pygame.font.Font(None, 36)
        
        self.ui_manager = pygame_gui.UIManager((self.game_world.width, self.game_world.height))
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), (100, 50)),
            text='Back',
            manager=self.ui_manager
        )
    
    def generate_planets(self):
        colors = [
        (255, 0, 0),   # Red (Fight)
        (0, 255, 0),   # Green (Artifact)
        (0, 0, 255),   # Blue (Shop)
        (255, 0, 255), # Magenta (Mystery)
        ]

        weigthed_colors = [0.7, 0.1, 0.1, 0.1]
        colors = random.choices(colors, weights=weigthed_colors, k=10)

        planet_names = [
        "Mercury", "Venus", "Earth", "Mars", "Jupiter",
        "Saturn", "Uranus", "Neptune", "Pluto", "Eris"
    ]

        max_attempts = 100  # Max tries to find non-overlapping position per planet

        for i in range(10):
            name = planet_names[i]
            size = random.randint(35, 50)
            color = random.choice(colors)

            placed = False
            for attempt in range(max_attempts):
                x = random.randint(size + 10, self.game_world.width - size - 10)
                y = random.randint(size + 10, self.game_world.height - size - 10)
                new_pos = (x, y)

                overlaps = False
                for other in self.planets:
                    other_pos = other.transform.position
                    other_planet = other.get_component("Planet")
                    if other_planet is None:
                        continue
                    other_size = other_planet.size

                    dx = other_pos[0] - x
                    dy = other_pos[1] - y
                    distance = (dx**2 + dy**2)**0.5

                    if distance < (size + other_size + 10):
                     overlaps = True
                     break

                if not overlaps:
                    planet = GameObject(new_pos)
                    planet.add_component(Planet(name, size, color, new_pos, self.game_world))
                    self.planets.append(planet)
                    self.game_world._gameObjects.append(planet)
                    placed = True
                    break

    def draw(self, screen):
        for planet in self.planets:
            planet.draw(screen, self.font)