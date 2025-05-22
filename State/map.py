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
    
    def generate_planets(self, planet_specs=None):
        self.planets.clear()
        if planet_specs is not None:
            for spec in planet_specs:
                planet = GameObject(spec['position'])
                planet.add_component(Planet(
                    spec['name'],
                    spec['size'],
                    spec['color'],
                    spec['position'],
                    self.game_world
                ))
                self.planets.append(planet)
                self.game_world._gameObjects.append(planet)
        else:
            # Default: generate 10 random planets
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
            for i in range(10):
                name = planet_names[i]
                size = random.randint(35, 50)
                color = random.choice(colors)
                x = random.randint(size + 10, self.game_world.width - size - 10)
                y = random.randint(size + 10, self.game_world.height - size - 10)
                position = (x, y)
                planet = GameObject(position)
                planet.add_component(Planet(name, size, color, position, self.game_world))
                self.planets.append(planet)
                self.game_world._gameObjects.append(planet)

    def load_planets(self, planet_rows):
        self.planets.clear()
        for row in planet_rows:
            name, type, explored, x, y, size, r, g, b = row
            position = (x, y)
            color = (r, g, b)
            planet = GameObject(position)
            planet.add_component(Planet(name, size, color, position, self.game_world))
            self.planets.append(planet)
            self.game_world._gameObjects.append(planet)

    def draw(self, screen):
        for planet in self.planets:
            planet.draw(screen, self.font)


            planet_component = planet.get_component("Planet")
            if planet_component:
                planet.draw(screen, self.font)

    def check_and_spawn_boss(self):
        pass