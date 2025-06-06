import pygame
import pygame_gui
from UI.currency import Currency

class RewardScreen:
    def __init__(self, game_world,):
        self.game_world = game_world
        self.currency = Currency()
        

        self.gained_credits = 25
        self.gained_scraps = 10

        self.credit_img = pygame.image.load("Assets/Icons/credit.png").convert_alpha()
        self.scrap_img = pygame.image.load("Assets/Icons/scrap.png").convert_alpha()

        self.screen_size = (game_world.width, game_world.height)
        self.ui_manager = pygame_gui.UIManager(self.screen_size)
        

        # Opret pygame_gui knap
        self.continue_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(500, 400, 200, 50),
            text="Continue",
            manager=self.ui_manager
        )

        self.font = pygame.font.Font(None, 36)

    def handle_event(self, event):
        self.ui_manager.process_events(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.continue_button:
            self.gain_reward(self.gained_credits, self.gained_scraps)
            self.game_world._game_state = "map"
            

    def gain_reward(self, credits, scraps):
        self.currency.addCredit(credits)
        self.currency.addScrap(scraps)
        # Log the gained rewards
        print(f"Gained Credits: {self.gained_credits}, Gained Scraps: {self.gained_scraps}")


    def update(self, time_delta):
        self.ui_manager.update(time_delta)

    def draw(self, screen):
        screen.fill((0, 0, 0))

        # Tekst og billeder
        title = self.font.render("Rewards", True, (255, 255, 255))
        screen.blit(title, (400, 50))

        screen.blit(self.credit_img, (350, 100))
        credits_text = self.font.render(f"Credits: 50", True, (255, 255, 255)) # Adjusted to match gained_credits {self.gained_credits}
        screen.blit(credits_text, (400, 100))

        screen.blit(self.scrap_img, (350, 150))
        scraps_text = self.font.render(f"Scraps: 20", True, (255, 255, 255)) # Adjusted to match gained_scraps {self.gained_scraps}
        screen.blit(scraps_text, (400, 150))

        # Tegn UI
        self.ui_manager.draw_ui(screen)
