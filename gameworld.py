import pygame
from menu import Menu
from gameobject import GameObject
from FactoryPatterns.cardfactory import CardFactory

class GameWorld:
    def __init__(self):
        pygame.mixer.init()
        pygame.init()
    
        self.width = 720
        self.height = 500
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game World")
        self._running = True
        self._clock = pygame.time.Clock()
        self._gameObjects = []
        self._cardFactory = CardFactory()
        self._create_card = False

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

            self.screen.fill("black")

            delta_time = self._clock.tick(60) / 1000.0

            for gameObject in self._gameObjects[:]:
                gameObject.update(delta_time)

            self._gameObjects = [obj for obj in self._gameObjects if not obj.is_destroyed]

            if self._create_card == False:
                card = self._cardFactory.create_component()
                self.instantiate(card)
                self._create_card = True

            pygame.display.flip()
            self._clock.tick(60)

        pygame.quit()

Menu().run()
