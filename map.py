import pygame
import random

from Components.planet import Planet
from gameobject import GameObject

#Made by Erik
# This code is a simple game map with planets and a spaceship.
# The player can move the spaceship around the map and interact with planets.

class Map:
    def __init__(self, game_world):
        self._game_world = game_world
        self._planet_list = []
        
    def generate_planets(self, player):
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
                position = (
                    random.randint(size + 10, self._game_world.width - size - 10),
                    random.randint(size + 10, self._game_world.height - size - 10)
                )
                go_planet = GameObject(position)
                go_planet.add_component(Planet(name, size, color, position, gameworld=self._game_world))
                self._game_world.instantiate(go_planet)
                self._planet_list.append(go_planet)
                print(f"Planet {name} created at {position} with size {size} and color {color}")