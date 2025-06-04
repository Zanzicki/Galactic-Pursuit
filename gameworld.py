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
from GameState.map import Map
from GameState.shop import Shop
from Components.planet import Planet
from UI.uimanager import UIManager
from UI.turnorder import TurnOrder
from UI.uielement import UIElement
from GameState.startgame import NewGame
from GameState.endgamescreen import EndGameScreen
from ObjectPool.pool import ReusablePool
from soundmanager   import SoundManager
from BuilderPattern.bossbuilder import BossBuilder

class GameWorld:
    def __init__(self, width, height):
        # --- Pygame and Window Setup ---
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Galactic Pursuit")
        self._clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self._running = True

        # --- Game State ---
        self._game_state = "menu"
        self.state_changed_to_shop = "out"
        self._fight_initialized = False

        # --- Core Game Objects and Factories ---
        self._gameObjects = []
        self._cardFactory = CardFactory()
        self._artifactFactory = ArtifactFactory()
        self._enemyFactory = EnemyFactory()
        self.card_pool = ReusablePool(10)

        # --- UI and Managers ---
        self.ui_element = UIElement(self.screen)
        self.card_pool = ReusablePool(10)  # Initialize the object pool
        self._fight_initialized = False  # Flag to check if fight has been initialized
        SoundManager().play_music()  # Play background music

        # Initialize UIManager
        self.ui_manager = UIManager(self)

        # --- Player Setup ---
        builder = PlayerBuilder()
        builder.build()
        self.playerGo = builder.get_gameObject()
        self.player = builder.player
        Player._instance = self.player  # Ensure singleton
        self._gameObjects.append(self.playerGo)
        self.player.deck.create_starter_deck()
        builder.get_gameObject().transform.position = pygame.math.Vector2(self.width // 2, self.height // 2)

        # --- World and State Objects ---
        self.map = Map(self)
        self.shop = Shop(self)
        self.start_game = NewGame(self)
        self.end_game = EndGameScreen(self)
        self.turn_order = None
        self.current_enemy = None

        self.state_icons = {
            "attack": pygame.image.load("Assets/Icons/attack.png").convert_alpha(),
            "defend": pygame.image.load("Assets/Icons/defend.png").convert_alpha(),
            "skill": pygame.image.load("Assets/Icons/skill.png").convert_alpha(),
        }
        

    # --- Properties ---
    @property
    def GameState(self):
        return self._game_state

    @GameState.setter
    def GameState(self, value):
        self._game_state = value

    def awake(self):
        for gameObject in self._gameObjects:
            gameObject.awake(self)

    def start(self):
        for gameObject in self._gameObjects:
            gameObject.start()

    # --- GameObject Management ---
    def instantiate(self, gameObject):
        gameObject.awake(self)
        gameObject.start()
        self._gameObjects.append(gameObject)
        # print(f"Instantiated GameObject: {gameObject}")

    # --- Game Loop ---
    def update(self):
        while self._running:
            delta_time = self._clock.tick(60) / 1000.0
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self._running = False
                self.ui_manager.handle_event(event)
                if self._game_state == "shop":
                    self.shop.handle_event(event)
                    
            pygame.pressed_keys = pygame.key.get_pressed()
            if pygame.pressed_keys[pygame.K_ESCAPE]:
                self._running = False

            self.screen.fill("black")
            self._handle_state(delta_time, events)
            self._cleanup_destroyed_objects()
            self._debug_gameobject_list()
            pygame.display.flip()
        pygame.quit()

    # --- State Handling ---
    def _handle_state(self, delta_time, events):
        match self._game_state:
            case "menu":
                self.ui_manager.show_menu_buttons()
                self.ui_manager.hide_game_buttons()
                self.ui_manager.update(delta_time)
                self.ui_manager.draw(self.screen)
            case "map":
                pygame.draw.circle(self.screen, (255, 223, 0), (400, 300), 100)
                self.draw_and_update_map(delta_time, events)
                self.ui_manager.hide_game_buttons()
            case "shop":
                if self.state_changed_to_shop == "into":
                    self.state_changed_to_shop = "in"
                    self.shop.enter()
                self.shop.update(delta_time)
                self.shop.draw()
                if self.state_changed_to_shop == "out":
                    self._game_state = "map"
                    self.shop.exit()
            case "game":
                self.ui_manager.show_game_buttons()
                self.draw_and_update_fight(delta_time, events, boss_fight=False)
                self.back_to_map(delta_time)
            case "game_over":
                self._draw_centered_text("Game Over", (255, 0, 0))
            case "artifact":
                self._draw_centered_text("Artifact", (255, 0, 0))
                self.back_to_map(delta_time)
            case "mystery":
                self._draw_centered_text("Mystery", (255, 0, 0))
                self.back_to_map(delta_time)
            case "end_game":
                self.end_game.update(delta_time, events)
                self.end_game.draw(self.screen)
            case "boss_fight":
                self.ui_manager.show_game_buttons()
                self.draw_and_update_fight(delta_time, events, boss_fight=True)
                self.back_to_map(delta_time)
            case _:
                print(f"Unknown game state: {self._game_state}")

        # Update artifacts (if not in menu)
        if self._game_state != "menu":
            for gameObject in self._gameObjects:
                if gameObject.get_component("Artifact") is not None:
                    gameObject.update(delta_time)
            self.ui_manager.hide_menu_buttons()


    def _draw_centered_text(self, text, color):
        self.screen.fill((0, 0, 0))
        rendered = self.font.render(text, True, color)
        self.screen.blit(rendered, (self.width // 2 - rendered.get_width() // 2,
                                    self.height // 2 - rendered.get_height() // 2))

    def _cleanup_destroyed_objects(self):
        self._gameObjects = [obj for obj in self._gameObjects if not obj.is_destroyed]

    def _debug_gameobject_list(self):
        pygame.pressed_keys = pygame.key.get_pressed()
        if pygame.pressed_keys[pygame.K_g]:
            print("GameObjects in GameWorld:")
            for gameObject in self._gameObjects:
                if gameObject.get_component("artifact") is not None:
                    print(f"Artifact: {gameObject.get_component('artifact')._name}")

    # --- Map and Fight Logic ---
    def draw_and_update_map(self, delta_time, events):
        for gameObject in self._gameObjects:
            if gameObject.get_component("Planet") is not None:
                gameObject.update(delta_time)
                gameObject.get_component("Planet").draw(self.screen, self.font)
        self.ui_element.draw("Solar system", (640, 40), self.player._credits, self.player._scraps, self.player._health, self.player._max_health)
        for gameObject in self._gameObjects:
            if gameObject.get_component("Player") is not None:
                gameObject.get_component("Player").get_events(events)
                gameObject.update(delta_time)
        self.map.check_player_planet_interaction(self.player, events)

    def draw_and_update_fight(self, delta_time, events, boss_fight=False):
        # Initialize fight if needed
        if boss_fight:
            if not hasattr(self, "_boss_fight_initialized") or not self._boss_fight_initialized:
                self._initialize_fight(boss_fight=True)
        else:
            if not hasattr(self, "_fight_initialized") or not self._fight_initialized:
                self._initialize_fight(boss_fight=False)

        # Draw UI
        self.ui_element.draw(
            f"Turn: {getattr(self, 'turn_count', 1)}", (self.width // 2, 40),
            self.player._credits, self.player._scraps,
            self.player._health + self.player.temp_health, self.player._max_health, self.player.temp_health
        )

        # Draw cards and enemy/boss
        for gameObject in self._gameObjects:
            if gameObject.get_component("CardDisplay") is not None:
                gameObject.update(delta_time)
                gameObject.get_component("CardDisplay").draw_cardtext(self.screen, gameObject)

            if boss_fight and gameObject.get_component("Boss") is not None:
                boss = gameObject.get_component("Boss")
                gameObject.update(delta_time)
                boss_x = self.width // 2
                boss_y = self.height // 3
                gameObject.transform.position = (
                    boss_x - gameObject.get_component("SpriteRenderer").sprite_image.width / 2,
                    boss_y - gameObject.get_component("SpriteRenderer").sprite_image.height / 2
                )
                boss.draw(
                    self.screen,
                    gameObject.transform.position,
                    gameObject.get_component("SpriteRenderer")._sprite_image
                )
                healthbar_pos = (boss_x - 100, boss_y - 100)
                self.ui_element.draw_healthbar(
                    self.screen,
                    boss.health,
                    boss._max_health,
                    healthbar_pos
                )
                icon_type = boss.get_state_icon()
                if icon_type and icon_type in self.state_icons:
                    icon_img = self.state_icons[icon_type]
                    sprite_rect = gameObject.get_component("SpriteRenderer").sprite_image.get_rect(topleft=gameObject.transform.position)
                    icon_x = boss_x - icon_img.get_width() // 2 - 150
                    icon_y = boss_y - icon_img.get_height() / 2 - 80
                    self.screen.blit(icon_img, (icon_x, icon_y))

            elif not boss_fight and gameObject.get_component("Enemy") is not None:
                enemy = gameObject.get_component("Enemy")
                gameObject.update(delta_time)
                enemy_x = self.width // 2
                enemy_y = self.height // 3
                gameObject.transform.position = (enemy_x - 75, enemy_y - 75)
                enemy.draw(self.screen, gameObject.transform.position, gameObject.get_component("SpriteRenderer")._sprite_image)
                healthbar_pos = (enemy_x - 100, enemy_y - 100)
                self.ui_element.draw_healthbar(
                    self.screen,
                    enemy.health,
                    enemy._max_health,
                    healthbar_pos
                )

        # Draw hand if needed
        if not hasattr(self, "_hand_drawn") or not self._hand_drawn:
            self.player.deck.draw_hand()
            for card in self.player.deck.hand:
                print(f"Card drawn: {card._name} - Type: {card._type} - Value: {card._value}")
            self.draw_cards(self.player.deck)
            self._hand_drawn = True

        # Handle events
        for event in events:
            self.ui_manager.handle_event(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.ui_manager.end_turn_button:
                player_deck = self.player.deck
                player_deck.discard_hand()
                if boss_fight:
                    self.current_boss.boss_action()
                else:
                    self.current_enemy.enemy_action()
                if not hasattr(self, "turn_count"):
                    self.turn_count = 1
                self.turn_count += 1
                self._hand_drawn = False
                self.ui_manager.hide_end_turn_button()

    def _initialize_fight(self, boss_fight=False):
        print("Initializing fight...")
        # Remove previous enemies and bosses
        for gameObject in self._gameObjects:
            if gameObject.get_component("Enemy") is not None or gameObject.get_component("Boss") is not None:
                gameObject.destroy()
        self._gameObjects = [obj for obj in self._gameObjects if not obj.is_destroyed]

        # Reset deck
        self.turn_count = 1
        self.player.deck.initialize_draw_pile()
        self.player.deck.draw_hand()
        self.draw_cards(self.player.deck)
        self._hand_drawn = True

        if boss_fight:
            boss_builder = BossBuilder("Gorkron the Destroyer", 20, 100)
            boss_builder.build()
            boss_game_object = boss_builder.get_gameObject()
            self.instantiate(boss_game_object)
            self.current_boss = boss_game_object.get_component("Boss")
            self._boss_fight_initialized = True
            self._fight_initialized = True
        else:
            random_enemy = random.choice(["Arangel", "Gorpi", "The Blue Centipede"])
            new_enemy = self._enemyFactory.create_component(random_enemy)
            self.instantiate(new_enemy)
            self.current_enemy = new_enemy.get_component("Enemy")
            self.turn_order = TurnOrder(self.player, self.current_enemy)
            self._fight_initialized = True
            self._boss_fight_initialized = False

    def get_player_position(self):
        if self.playerGo and self.playerGo.transform:
            return self.playerGo.transform.position
        return pygame.math.Vector2(self.width // 2, self.height // 2)
    
    def draw_cards(self, player_deck):
        # Remove old card GameObjects
        for obj in self._gameObjects:
            if obj.get_component("CardDisplay") is not None:
                obj.is_destroyed = True
        self._cleanup_destroyed_objects()

        # Ensure card_positions is long enough
        hand_size = len(player_deck.hand)
        if len(self.player.deck.card_positions) < hand_size:
            # Generate positions for all cards in hand
            self.player.deck.card_positions = [
                pygame.math.Vector2(
                    200 + i * 180,  # X position (adjust spacing as needed)
                    self.height - 200  # Y position
                ) for i in range(hand_size)
            ]

        for i, card in enumerate(player_deck.hand):
            card_game_object = self.card_pool.acquire()
            if card_game_object is None:
                card_game_object = self._cardFactory.create_component(card)
            else:
                # Just update the CardDisplay's reference, do NOT overwrite fields!
                card_game_object.get_component("CardDisplay").card_data = card
                card_game_object.is_destroyed = False

            self.instantiate(card_game_object)
            card_game_object.transform.position = self.player.deck.card_positions[i]

    def back_to_map(self, delta_time):
        self.ui_manager.back_to_map_button.show()
        self.ui_manager.update(delta_time)
        self.ui_manager.draw(self.screen)

