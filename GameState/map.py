import pygame
import random
import pygame_gui
from Components import planet
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
        def is_overlapping(new_pos, new_size):
            for existing_planet in self.planets:
                existing_transform = existing_planet.transform
                if not existing_transform or not hasattr(existing_transform, "position"):
                    continue
                existing_pos = existing_transform.position
                existing_size = existing_planet.get_component("Planet")._size
                dx = new_pos[0] - existing_pos[0]
                dy = new_pos[1] - existing_pos[1]
                distance = (dx**2 + dy**2) ** 0.5
                if distance < new_size + existing_size + 10:
                    return True
            return False

        self.planets.clear()
        self.game_world._gameObjects = [
            obj for obj in self.game_world._gameObjects
            if obj.get_component("Planet") is None
    ]

        planet_names = [
        "Mercury", "Venus", "Earth", "Mars", "Jupiter",
        "Saturn", "Uranus", "Neptune", "Pluto", "Eris"
    ]

        required_colors = [
        (255, 0, 0),   # Red (Fight)
        (0, 255, 0),   # Green (Artifact)
        (0, 0, 255),   # Blue (Shop)
        (255, 0, 255), # Magenta (Mystery)
    ]

        all_colors = required_colors.copy()
        extra_colors = random.choices(all_colors, k=6)
        colors_to_use = required_colors + extra_colors

        for i in range(10):
            name = planet_names[i]
            size = random.randint(35, 50)
            color = colors_to_use[i]

            max_attempts = 100
            position = None
            for attempt in range(max_attempts):
                x = random.randint(size + 10, self.game_world.width - size - 10)
                y = random.randint(size + 10, self.game_world.height - size - 10)
                candidate = (x, y)
                if not is_overlapping(candidate, size):
                    position = candidate
                    break

            if position is None:
                print(f" Kunne ikke placere planet '{name}' uden overlap efter {max_attempts} forsøg.")
                continue

            planet = GameObject(position)
            if not planet.transform or not hasattr(planet.transform, "position"):
                print(f"Fejl: transform ikke initialiseret korrekt på planet {name}")
                continue

        # Sikrer at transform.position sættes korrekt (hvis ikke allerede gjort)
            planet.transform.position = pygame.math.Vector2(position)

            planet.add_component(Planet(name, size, color, position, self.game_world))
            self.planets.append(planet)
            self.game_world._gameObjects.append(planet)

            print(f" Placerede planet '{name}' ved {position} med farve {color}")



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

    def check_and_spawn_boss(self):
        print("are you being called?")
        if all(planet.get_component("Planet").visited for planet in self.planets):
            print("All planets visited. Spawning boss...")
            
            if any(p.get_component("Planet").name == "Boss" for p in self.planets):
                
                return

            boss_size = 70
            boss_color = (205, 127, 50)
            boss_position = (self.game_world.width // 2, 100)
            boss = GameObject(boss_position)
            boss.add_component(Planet("Boss", boss_size, boss_color, boss_position, self.game_world))
            self.planets.append(boss)
            self.game_world._gameObjects.append(boss)

    def draw(self, screen):
        for planet in self.planets:
            planet_component = planet.get_component("Planet")
            if planet_component:
                planet.draw(screen, self.font)
