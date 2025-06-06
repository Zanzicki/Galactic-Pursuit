import pygame
import random

class StarBackground:
    def __init__(self, width, height, num_stars=100):
        self.width = width
        self.height = height
        self.num_stars = num_stars
        self.stars = []
        for _ in range(self.num_stars):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            speed = random.uniform(0.5, 2.5)
            self.stars.append([x, y, speed])

    def update(self):
        for star in self.stars:
            star[1] += star[2]
            if star[1] > self.height:
                star[0] = random.randint(0, self.width)
                star[1] = 0
                star[2] = random.uniform(0.5, 2.5)

    def draw(self, screen):
        for star in self.stars:
            screen.set_at((int(star[0]), int(star[1])), (255, 255, 255))