import pygame
import random
from BuilderPattern.playerbuilder import PlayerBuilder
from menu import Menu
from gameobject import GameObject
from FactoryPatterns.cardfactory import CardFactory
from FactoryPatterns.artifactFactory import ArtifactFactory
from Components.deck import Deck
from UIManager import UIManager
from FactoryPatterns.enemyfactory import EnemyFactory
from map import Map
from shop import Shop
from Components.planet import Planet

class GameWorld:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Galactic Pursuit")
        self._running = True
        self._state = "map"  # Start in the map state
        self._clock = pygame.time.Clock()
        self._gameObjects = []  # List of all game objects
        self.font = pygame.font.Font(None, 36)
        self._cardFactory = CardFactory()
        self._artifactFactory = ArtifactFactory()
        self._deck = Deck()
        self._create_card = False
        self.ui_manager = UIManager()
        self.menu = Menu(self)  # Pass GameWorld to the Menu
        self._enemyFactory = EnemyFactory()

        builder = PlayerBuilder()
        builder.build()
        
        self._gameObjects.append(builder.get_gameObject())
        self.player = builder.get_gameObject 
        self.map = Map(self)  # Pass GameWorld to the Map
        self.shop = Shop(self)  # Pass GameWorld to the Shop

        # Initialize player and planets
        self.map.generate_planets(self.player)
        self.player_position = [400, 300]  # Example player position

    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, value):
        self._state = value

    def instantiate(self, gameObject):
        gameObject.awake(self)
        gameObject.start()
        self._gameObjects.append(gameObject)

    def awake(self):
        for gameObject in self._gameObjects[:]:
            gameObject.awake(self)

    def start(self):
        for gameObject in self._gameObjects[:]:
            gameObject.start()

    def update(self):
        while self._running:
            delta_time = self._clock.tick(60) / 1000.0  # Limit to 60 FPS

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False

                # Handle button events
                self.ui_manager.handle_event(event)

            self.screen.fill("black")

            delta_time = self._clock.tick(60) / 1000.0

            # Update all game objects
            for gameObject in self._gameObjects[:]:
                gameObject.update(delta_time)
                if gameObject.get_component("Planet") is not None:
                   gameObject.get_component("Planet").draw(self.screen, self.font)

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

            pygame.draw.circle(self.screen, (255, 223, 0), (400, 300), 100)  # Sun in the center

            self._gameObjects = [obj for obj in self._gameObjects if not obj.is_destroyed]
            
            pygame.display.flip()
            self._clock.tick(60)

        pygame.quit()

    def draw(self):
        self.screen.fill("black")

        self.ui_manager.draw_card_screen(self.screen)
        pygame.display.flip()

    def get_player_position(self):
        for gameObject in self._gameObjects:
                if gameObject.get_component("Player") is not None:
                    return gameObject.transform.position
    