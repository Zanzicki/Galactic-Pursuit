import pygame
import pygame_gui


class UIManager:
    def __init__(self, game_world):
        self.game_world = game_world  # Reference to the GameWorld
        self.ui_manager = pygame_gui.UIManager((game_world.width, game_world.height))  # Initialize pygame_gui UI manager
        self.screen = game_world.screen

        # Example buttons for the menu
        self.play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen.width/2-200, self.screen.height/2-250), (400, 100)),
            text="PLAY",
            manager=self.ui_manager
        )
        self.options_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen.width/2-200, self.screen.height/2-50), (400, 100)),
            text="OPTIONS",
            manager=self.ui_manager
        )
        self.quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen.width/2-200, self.screen.height/2+150), (400, 100)),
            text="QUIT",
            manager=self.ui_manager
        )

        self.back_to_map_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((550, 500), (200, 50)),
            text="RETURN TO MAP",
            manager=self.ui_manager,
            visible=False 
        )

    def handle_event(self, event):
        self.ui_manager.process_events(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.play_button:
                self.start_game()
            elif event.ui_element == self.quit_button:
                self.quit_game()
            elif event.ui_element == self.back_to_map_button:
                self.return_to_map()

    def update(self, delta_time):
        self.ui_manager.update(delta_time)

    def draw(self, screen):
        self.ui_manager.draw_ui(screen)

    def start_game(self):
        print("Starting Game")
        self.game_world.state = "map"  # Transition to the map state
        self.play_button.hide()
        self.options_button.hide()
        self.quit_button.hide()

    def quit_game(self):
        print("Quitting Game")
        self.game_world._running = False

    def return_to_map(self):
        print("Returning to Map")
        self.game_world.state = "map"
        self.back_to_map_button.hide()
    
    def show_options(self):
        print("Showing Options")
        # Implement options menu logic here

    # Draws the health bar of a game object
    def draw_healthbar(self, screen, max_health, position):
        bar_width = 200
        bar_height = 20
        x, y = position

        health_percentage = max_health / 100
        
        pygame.draw.rect(screen, (255, 0, 0), (x, y, bar_width, bar_height))

        pygame.draw.rect(screen, (0, 255, 0), (x, y, bar_width * health_percentage, bar_height))