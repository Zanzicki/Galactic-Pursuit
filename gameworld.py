import pygame
from menu import Menu
from gameobject import GameObject
from FactoryPatterns.cardfactory import CardFactory
from FactoryPatterns.artifactFactory import ArtifactFactory
from Components.deck import Deck
from UIManager import UIManager
from FactoryPatterns.enemyfactory import EnemyFactory
from map import Map
from shop import Shop


class GameWorld:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Galactic Map")
        self._running = True
        self._state = "menu"  # Start in the menu state
        self._clock = pygame.time.Clock()
        self._gameObjects = []
        self._cardFactory = CardFactory()
        self._artifactFactory = ArtifactFactory()
        self._deck = Deck()
        self._create_card = False
        self.ui_manager = UIManager()
        self.menu = Menu(self)  # Pass GameWorld to the Menu
        self._enemyFactory = EnemyFactory()
        self.map = Map(self)  # Pass GameWorld to the Map
        self.shop = Shop(self)  # Pass GameWorld to the Shop

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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

                # Handle button events
                self.ui_manager.handle_event(event)

            # Handle the current state
            if self._state == "menu":
                self.menu.run()
            elif self._state == "map":
                self.map.run()
            elif self._state == "game":
                self.run_game()
            elif self._state == "shop":
                self.shop.run()

        pygame.quit()

    def run_game(self):
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
            new_enemy = self._enemyFactory.create_component("Arangel")
            self.instantiate(new_enemy)
            new_enemy.get_component("Enemy").enemy_action()

        self.ui_manager.draw_card_screen(self.screen)
        pygame.display.flip()