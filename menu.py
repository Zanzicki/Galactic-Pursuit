import pygame
import pygame_gui

class Menu:
    def __init__(self, game_world):
        self.game_world = game_world  # Reference to the GameWorld
        self.screen = game_world.screen
        self.ui_manager = pygame_gui.UIManager((game_world.width, game_world.height))  # Initialize pygame_gui UI manager

        # Create buttons for the menu
        self.play_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((260, 150), (200, 50)),
            text="PLAY",
            manager=self.ui_manager
        )
        self.options_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((260, 250), (200, 50)),
            text="OPTIONS",
            manager=self.ui_manager
        )
        self.quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((260, 350), (200, 50)),
            text="QUIT",
            manager=self.ui_manager
        )

    def handle_event(self, event):
        """Handle events for the menu."""
        print(f"Event: {event}")  # Debugging
        self.ui_manager.process_events(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            print(f"Button Pressed: {event.ui_element.text}")  # Debugging
            if event.ui_element == self.play_button:
                self.start_game()
            elif event.ui_element == self.options_button:
                self.open_options()
            elif event.ui_element == self.quit_button:
                self.quit_game()

    def update(self, delta_time):
        """Update the UI manager."""
        self.ui_manager.update(delta_time)

    def draw(self, screen):
        """Draw the menu."""
        screen.fill((30, 30, 30))  # Background color
        self.ui_manager.draw_ui(screen)

    def start_game(self):
        print("Starting Game")
        self.game_world.state = "map"  # Transition to the map state

    def open_options(self):
        print("Opening Options")
        self.game_world.state = "options"  # Transition to the options state

    def quit_game(self):
        print("Quitting Game")
        self.game_world._running = False
