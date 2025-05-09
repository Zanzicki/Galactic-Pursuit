import pygame
from UIManager import UIManager

class Menu:
    def __init__(self, game_world):
        self.game_world = game_world  # Reference to the GameWorld
        self.screen = game_world.screen
        self.running = True
        self.ui_manager = UIManager()

        # Define buttons for the menu
        self.ui_manager.set_buttons([
            {"text": "PLAY", "x": 260, "y": 150, "width": 200, "height": 50, "action": self.start_game},
            {"text": "OPTIONS", "x": 260, "y": 250, "width": 200, "height": 50, "action": self.open_options},
            {"text": "QUIT", "x": 260, "y": 350, "width": 200, "height": 50, "action": self.quit_game},
        ])

    def start_game(self):
        print("Starting Game")
        self.running = False  # Stop the menu loop
        self.game_world.start_game()  # Notify GameWorld to start the game

    def open_options(self):
        print("Opening Options")
        options_menu = Options()
        options_menu.run()

    def quit_game(self):
        print("Quitting Game")
        self.running = False
        self.game_world._running = False  # Stop the entire game
    
    def draw_card(self):
        print("Drawing Card")

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                    return

                self.ui_manager.handle_event(event)

            self.screen.fill((30, 30, 30))
            self.ui_manager.draw(self.screen)
            pygame.display.flip()

        


class EndGameMenu:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(EndGameMenu, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            pygame.init()
            self.screen = pygame.display.set_mode((400,300))
            self.font = pygame.font.Font(None, 36)
            self.running = True
            self._initialized = True

    def run(self):
        while self.running:
                self.screen.fill((50, 50, 50))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    UIManager().handle_endgame(event)

                UIManager().draw_end_screen(self.screen)
                pygame.display.flip()

class Options:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((720, 500))
        pygame.display.set_caption("Options")
        self.running = True
        self.ui_manager = UIManager()

        # Define buttons for the options menu
        self.ui_manager.set_buttons([
            {"text": "BACK", "x": 260, "y": 350, "width": 200, "height": 50, "action": self.quit_options},
        ])

    def quit_options(self):
        print("Returning to Main Menu")
        self.running = False

    def run(self):
        while self.running:
            self.screen.fill((50, 50, 50))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_options()
                self.ui_manager.handle_event(event)

            self.ui_manager.draw(self.screen)
            pygame.display.flip()
    
    class Combat():
        def __init__(self):
            pygame.init()
            self.screen = pygame.display.set_mode((720, 500))
            pygame.display.set_caption("Combat")
            self.running = True
            self.ui_manager = UIManager()

            # Define buttons for the combat menu
            self.ui_manager.set_buttons([
                {"text": "Draw", "x": 260, "y": 350, "width": 200, "height": 50, "action": self.draw_card},
            ])

        def draw_card(self):
            print("Drawing Card")
