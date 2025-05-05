import pygame
from menu import Menu
from gameobject import GameObject

class GameWorld:
    def __init__(self, width, height):
        pygame.mixer.init()
        pygame.init()
    
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game World")
        self._running = True
        self._clock = pygame.time.Clock()

    def instantiate(self, gameObject):
        gameObject.awake(self)
        gameObject.start()
        self._gameObjects.append(gameObject)
    
    def Awake(self): 
        for gameObject in self._gameObjects[:]:
            gameObject.awake(self)      
    
    def Start(self): 
        for gameObject in self._gameObjects[:]:
            gameObject.start()
    
    # Runs the core loop of the game, calls update on all gameobjects in the list, sets tick rate for fps, checks input for quitting the game,
    # draws the screen, checks collisions etc.
    def update(self):

        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running =False
            
            self._background.update()

            self._screen.fill("black")
            self._background.draw()

            delta_time = self._clock.tick(60) / 1000.0

            for gameObject in self._gameObjects[:]:
                gameObject.update(delta_time)

            self._gameObjects = [obj for obj in self._gameObjects if not obj.is_destroyed]
            self._colliders = [col for col in self._colliders if not col.gameObject.is_destroyed]

            pygame.display.flip()
            self._clock.tick(60)

        pygame.quit()

Menu().run()
