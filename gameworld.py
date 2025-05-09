import pygame
from menu import Menu
from gameObject import GameObject
from FactoryPatterns.cardfactory import CardFactory
from FactoryPatterns.artifactFactory import ArtifactFactory
from Components.deck import Deck
from UIManager import UIManager

class GameWorld:
    def __init__(self):
    
        self.width = 720
        self.height = 500
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game World")
        self._running = True
        self._clock = pygame.time.Clock()
        self._gameObjects = []
        self._cardFactory = CardFactory()
        self._artifactFactory = ArtifactFactory()
        self._deck = Deck()
        self._create_card = False
        self._ui_manager = UIManager()
        self._active_card = []  

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
                self._ui_manager.handle_back(event, self.go_back)
            self.screen.fill("black")

            delta_time = self._clock.tick(60) / 1000.0

            for gameObject in self._gameObjects[:]:
                gameObject.update(delta_time)

            self._gameObjects = [obj for obj in self._gameObjects if not obj.is_destroyed]

            if self._create_card == False:
                i = 0
                for card in self._deck.cards:
                    card = self._cardFactory.create_component(card)
                    self.instantiate(card)
                    card.transform.position = pygame.math.Vector2(100 + i, 250)
                    self._create_card = True
                    i += 50
                    self._active_card.append(card)
                     
                    
            self._ui_manager.draw_back_button(self.screen) 
            pygame.display.flip()
            self._clock.tick(60)

        
    def go_back(self):
        self._running = False
        from menu import Menu
        Menu().running = True 
        menu = Menu()
        menu.run()
        

pygame.mixer.init()
pygame.init() 
Menu().run()

