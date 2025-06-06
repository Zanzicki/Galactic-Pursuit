import pygame
import pygame_gui
from UI.currency import Currency

class RewardScreen:
    def __init__(self, game_world,):
        self.game_world = game_world
        self.currency = Currency()

        self.gained_credits = 50
        self.gained_scraps = 20

        self.credit_img = pygame.image.load("Assets/Icons/credit.png").convert_alpha()
        self.scrap_img = pygame.image.load("Assets/Icons/scrap.png").convert_alpha()

        self.screen_size = (game_world.width, game_world.height)
        self.ui_manager = pygame_gui.UIManager(self.screen_size)
        

        # Opret pygame_gui knap
        self.font = pygame.font.Font(None, 36)

        # Center the button horizontally
        button_width = 200
        button_height = 50
        button_x = (self.screen_size[0] - button_width) // 2
        button_y = 360  # You can adjust this value as needed

        self.continue_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(button_x, button_y, button_width, button_height),
            text="Continue",
            manager=self.ui_manager
        )

    def handle_event(self, event):
        self.ui_manager.process_events(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.continue_button:
            self.gain_reward(self.gained_credits, self.gained_scraps)
            self.game_world._game_state = "map"

    def gain_reward(self, credits, scraps):
        self.currency.addCredit(credits)
        self.currency.addScrap(scraps)

    def update(self, time_delta):
        self.ui_manager.update(time_delta)

    def draw(self, screen):
        center_x = self.screen_size[0] // 2

        # Title
        title = self.font.render("Rewards", True, (255, 255, 255))
        title_rect = title.get_rect(center=(center_x, 180))
        screen.blit(title, title_rect)

        # Credits icon and text
        credit_img_rect = self.credit_img.get_rect(center=(center_x - 60, 120))
        screen.blit(self.credit_img, credit_img_rect)
        credits_text = self.font.render(f"Credits: {self.gained_credits}", True, (255, 255, 255))
        credits_text_rect = credits_text.get_rect(midleft=(center_x, 240))
        screen.blit(credits_text, credits_text_rect)

        # Scraps icon and text
        scrap_img_rect = self.scrap_img.get_rect(center=(center_x - 60, 180))
        screen.blit(self.scrap_img, scrap_img_rect)
        scraps_text = self.font.render(f"Scraps: {self.gained_scraps}", True, (255, 255, 255))
        scraps_text_rect = scraps_text.get_rect(midleft=(center_x, 300))
        screen.blit(scraps_text, scraps_text_rect)

        self.ui_manager.draw_ui(screen)
