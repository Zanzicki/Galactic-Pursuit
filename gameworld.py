import pygame
from menu import Menu
from gameObject import GameObject
from FactoryPatterns.cardfactory import CardFactory
from FactoryPatterns.artifactFactory import ArtifactFactory
from Components.deck import Deck
from UIManager import UIManager
from UIManager import UIManager

class GameWorld:
    def __init__(self):
        pygame.init()
        self.width = 720
        self.height = 500
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game World")
        self._running = True
        self._in_menu = True  # Start in the menu
        self._clock = pygame.time.Clock()
        self._gameObjects = []
        self._cardFactory = CardFactory()
        self._artifactFactory = ArtifactFactory()
        self._deck = Deck()
        self._create_card = False
<<<<<<< HEAD
        self._ui_manager = UIManager()
        self._active_card = []  
        self.ui_manager = UIManager()
        self.menu = Menu(self)  # Pass GameWorld to the Menu
=======
        self._ui_manager = UIManager() 
>>>>>>> parent of 9bdbbb8 (Hover funktion and cart info works)

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

    def update(self):
        while self._running:
            if self._in_menu:
                # Run the menu
                self.menu.run()
            else:
                # Run the game
                self.run_game()

        pygame.quit()

    def run_game(self):
        while not self._in_menu and self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

                # Handle button events
                self.ui_manager.handle_event(event)

            self.screen.fill("black")

            delta_time = self._clock.tick(60) / 1000.0

            for gameObject in self._gameObjects[:]:
                gameObject.update(delta_time)

            self._gameObjects = [obj for obj in self._gameObjects if not obj.is_destroyed]

            if not self._create_card:
                i = 0
                for card in self._deck.cards:
                    card = self._cardFactory.create_component(card)
                    self.instantiate(card)
                    card.transform.position = pygame.math.Vector2(100 + i, 250)
                    self._create_card = True
                    i += 50  
<<<<<<< HEAD

            self.ui_manager.draw_card_screen(self.screen)
=======
                    
            self._ui_manager.draw_back_button(self.screen) 
>>>>>>> parent of 9bdbbb8 (Hover funktion and cart info works)
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

