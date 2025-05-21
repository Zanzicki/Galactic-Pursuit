import pygame
from gameworld import GameWorld

if __name__ == "__main__":
    pygame.init()
    game_world = GameWorld(1280, 720)
    game_world.awake()
    game_world.start()
    game_world.update()