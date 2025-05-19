import pygame
import pygame_gui


class UIManager:
    def __init__(self, game_world):
        self.game_world = game_world  # Reference to the GameWorld
        self.ui_manager = pygame_gui.UIManager((game_world.width, game_world.height))  # Initialize pygame_gui UI manager
        self.screen = game_world.screen

        self.new_game = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen.width/2-200, self.screen.height/2-250), (400, 100)),
            text="New Game",
            manager=self.ui_manager
        )

        self.continue_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen.width/2-200, self.screen.height/2-150), (400, 100)),
            text="CONTINUE",
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

        self.deck_tracker_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen.width/20, self.screen.height-200), (150, 150)),
            text="DECK\nTRACKER",
            manager=self.ui_manager,
            visible=False
        )

    def handle_event(self, event):
        self.ui_manager.process_events(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.continue_button:
                self.start_game()
            elif event.ui_element == self.new_game:
                self.start_new_game()
            elif event.ui_element == self.quit_button:
                self.quit_game()
            elif event.ui_element == self.back_to_map_button:
                self.return_to_map()
            elif event.ui_element == self.options_button:
                self.show_options()
            elif event.ui_element == self.deck_tracker_button:
                print("Deck Tracker Button Pressed")

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

    def start_new_game(self):
        print("Starting New Game")
        self.game_world.state = "map"
        
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

    def deck_tracker(self):
        print("Showing Deck Tracker")
        # Implement deck tracker logic here
        self.deck_tracker_button.show()

    # Draws the health bar of a game object
    def draw_healthbar(self, screen, max_health, position):
        bar_width = 200
        bar_height = 20
        x, y = position

        health_percentage = max_health / 100
        
        pygame.draw.rect(screen, (255, 0, 0), (x, y, bar_width, bar_height))

        pygame.draw.rect(screen, (0, 255, 0), (x, y, bar_width * health_percentage, bar_height))
        #draw health text
        font = pygame.font.Font(None, 24)
        health_text = font.render(f"Health: {max_health}", True, (255, 255, 255))
        text_rect = health_text.get_rect(center=(x + bar_width // 2, y + bar_height // 2))
        screen.blit(health_text, text_rect)
