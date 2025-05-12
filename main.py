import pygame
from gameworld import GameWorld

if __name__ == "__main__":
    pygame.init()
    game_world = GameWorld(800, 600)
    game_world.Awake()
    game_world.Start()
    game_world.update()