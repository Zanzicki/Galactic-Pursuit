import pygame
import random

import pygame_gui
from BuilderPattern.playerbuilder import PlayerBuilder
from Components.player import Player
from gameobject import GameObject
from FactoryPatterns.cardfactory import CardFactory
from FactoryPatterns.artifactFactory import ArtifactFactory
from Components.deck import Deck
from FactoryPatterns.enemyfactory import EnemyFactory
from State.map import Map
from State.shop import Shop
from Components.planet import Planet
from UI.uimanager import UIManager 
from turnorder import TurnOrder
from UI.uielement import UIElement 
from State.startgame import NewGame
from State.endgamescreen import EndGameScreen
from ObjectPool.pool import ReusablePool

class GameWorld:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Galactic Pursuit")
        self._running = True
        self._state = "menu"  # Start in the menu state
        self._clock = pygame.time.Clock()
        self._gameObjects = []  # List of all game objects
        self.font = pygame.font.Font(None, 36)
        self._cardFactory = CardFactory()
        self._artifactFactory = ArtifactFactory()
        self._deck = Deck()
        self._create_card = False
        self._enemyFactory = EnemyFactory()
        self.state_changed_to_shop = "out"
        self.turnorder = 0
        self.current_enemy = None
        self.ui_element = UIElement
        self.pool = ReusablePool(10)  # Initialize the object pool

        # Initialize UIManager
        self.ui_manager = UIManager(self)

        # Initialize Player using PlayerBuilder
        builder = PlayerBuilder()
        builder.build()
        self.playerGo = builder.get_gameObject()

        self.player = Player.get_instance()
        self._gameObjects.append(builder.get_gameObject())  # Add the player to the game objects

        # Center the player's position
        builder.get_gameObject().transform.position = pygame.math.Vector2(self.width // 2, self.height // 2)

        self.map = Map(self)
        self.shop = Shop(self)  # Pass GameWorld to the Shop
        self.start_game = NewGame(self)  # Pass GameWorld to the StartGame

        self.turn_order = None  # Will be set when a fight starts

        # Initialize the end game screen
        self.end_game = EndGameScreen(self)  # Pass GameWorld to the EndGameScreen

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

            events = pygame.event.get()  # Get all events for this frame
            for event in events:
                if event.type == pygame.QUIT:
                    self._running = False

                # Delegate UI events to the UIManager
                self.ui_manager.handle_event(event)
                if self.state == "shop":
                    self.shop.handle_event(event)
        
            pygame.pressed_keys = pygame.key.get_pressed()
            if pygame.pressed_keys[pygame.K_ESCAPE]:
                self._running = False

            self.screen.fill("black")

            if self._state == "menu":
                self.ui_manager.show_menu_buttons()
                self.ui_manager.hide_game_buttons()
                self.ui_manager.update(delta_time)
                self.ui_manager.draw(self.screen)
            else:
                self.ui_manager.hide_menu_buttons()

            if self._state == "map":
                pygame.draw.circle(self.screen, (255, 223, 0), (400, 300), 100)  # Sun in the center
                self.draw_and_update_map(delta_time, events)
                self.ui_manager.hide_game_buttons()
            elif self._state == "shop":
                if self.state_changed_to_shop == "into":
                    self.state_changed_to_shop = "in"
                    self.shop.enter()
                self.shop.update(delta_time)
                self.shop.draw()
                # When leaving shop and entering menu or map:
                if self.state_changed_to_shop == "out":
                    self.state = "map" 
                    self.shop.exit()
            elif self._state == "game":
                self.ui_manager.show_game_buttons()
                self.draw_and_update_fight(delta_time, events)
                self.back_to_map(delta_time)
            elif self._state == "game_over":
                self.screen.fill((0, 0, 0))
                game_over_text = self.font.render("Game Over", True, (255, 0, 0))
                self.screen.blit(game_over_text, (self.width // 2 - game_over_text.get_width() // 2,
                                                   self.height // 2 - game_over_text.get_height() // 2))
            elif self._state == "artifact":
                self.screen.fill((0, 0, 0))
                artifact_text = self.font.render("Artifact", True, (255, 0, 0))
                self.screen.blit(artifact_text, (self.width // 2 - artifact_text.get_width() // 2,
                                                   self.height // 2 - artifact_text.get_height() // 2))
                self.back_to_map(delta_time)
            elif self._state == "mystery":
                self.screen.fill((0, 0, 0))
                mystery_text = self.font.render("Mystery", True, (255, 0, 0))
                self.screen.blit(mystery_text, (self.width // 2 - mystery_text.get_width() // 2,
                                                   self.height // 2 - mystery_text.get_height() // 2))
                self.back_to_map(delta_time)

            elif self._state == "end_game":
                self.end_game.update(delta_time, events)
                self.end_game.draw(self.screen)

            if self._state != "game":
                 self._fight_initialized = False
                 
            self._gameObjects = [obj for obj in self._gameObjects if not obj.is_destroyed]

            pygame.display.flip()

        pygame.quit()

    def draw_and_update_map(self, delta_time, events):
        # First, update and draw planets
        for gameObject in self._gameObjects:
            if gameObject.get_component("Planet") is not None:
                gameObject.update(delta_time)
                gameObject.get_component("Planet").draw(self.screen, self.font)

        # Then, update and draw the player
        for gameObject in self._gameObjects:
            if gameObject.get_component("Player") is not None:
                gameObject.get_component("Player").get_events(events)
                gameObject.update(delta_time)

    def draw_and_update_fight(self, delta_time, events):
        # Setup fight if not already done
        if not hasattr(self, "_fight_initialized") or not self._fight_initialized:
            # Create cards and enemy as before
            self.draw_cards(self.player.deck)
            random_enemy = random.choice(["Arangel", "Gorpi", "The Blue Centipede"])
            new_enemy = self._enemyFactory.create_component(random_enemy)
            self.instantiate(new_enemy)
            self.current_enemy = new_enemy.get_component("Enemy")
            # Setup turn order
            self.turn_order = TurnOrder(self.player, self.current_enemy)
            self._fight_initialized = True

        turncount = self.turn_order.turncount
        self.ui_element.draw(self, f"{turncount}", (self.width // 2, 50))

        # Draw cards and enemy as before
        for gameObject in self._gameObjects:
            if gameObject.get_component("Card") is not None:
                gameObject.update(delta_time)
                gameObject.get_component("Card").draw_cardtext(self.screen, gameObject)
            if gameObject.get_component("Enemy") is not None:
                gameObject.update(delta_time)
                self.ui_element.draw_healthbar(self, self.screen, gameObject.get_component("Enemy").health, (300, 100))
        self.ui_element.draw_healthbar(self, self.screen, self.player.health, (self.width - 300, 100))

        # Turn logic
        if self.turn_order.is_player_turn():
            # Enable card play, show "End Turn" button, etc.
            self.ui_manager.show_end_turn_button()
            for event in events:
                self.ui_manager.handle_event(event)
                if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.ui_manager.end_turn_button:
                    self.turn_order.end_turn()
                    # When player ends turn:
                    player_deck = self.player.deck  # or wherever you access the player's deck
                    player_deck.discard_hand()
                    self.draw_cards(player_deck)
                    self.ui_manager.hide_end_turn_button()
        elif self.turn_order.is_enemy_turn():
            # Enemy acts automatically
            self.current_enemy.enemy_action()
            self.turn_order.end_turn()

    def draw_cards(self, player_deck):
        # Draw the player's cards
        player_hand = player_deck.draw_hand()
        for i in range(len(player_hand)):
            card = player_hand[i]
            card_game_object = self._cardFactory.create_component(card)
            self.instantiate(card_game_object)
            card_game_object.transform.position = self.player.deck.card_positions[i]

    def get_player_position(self):
        for gameObject in self._gameObjects:
                if gameObject.get_component("Player") is not None:
                    return gameObject.transform.position
                
    def back_to_map(self, delta_time):
                self.ui_manager.back_to_map_button.show()  
                self.ui_manager.update(delta_time)
                self.ui_manager.draw(self.screen)

