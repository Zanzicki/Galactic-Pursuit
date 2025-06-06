import pygame
from Components.button import Button
from UI.currency import Currency

class RewardScreen:
    def __init__(self, game_world):
        self.game_world = game_world
        self.font = pygame.font.Font(None, 36)
        self.reward_given = False
        self.currency = Currency()

        self.gained_credits = 50
        self.gained_scraps = 20

        self.credit_img = pygame.image.load("Assets/Icons/credit.png").convert_alpha()
        self.scrap_img = pygame.image.load("Assets/Icons/scrap.png").convert_alpha()

        self.continue_button = Button(500, 400, 200, 50, "Continue", (0, 255, 0), (0, 255, 0), (255, 255, 255), self.font)

    def handle_event(self, event):
        if self.countinue_button.is_clicked(event):
            self.game_world._game_state = "map"

    def update(self):
        if not self.reward_given:
            self.currency.addCredit(self.gained_credits)
            self.currency.addScrap(self.gained_scraps)
            self.reward_given = True
    
    def draw(self, screen):
        screen.fill((0, 0, 0))

        title = self.font.render("Rewards", True, (255, 255, 255))
        screen.blit(title, (400, 50))
        
        screen.blit(self.credit_img, (350, 50))
        credits_text = self.font.render(f"Credits: {self.gained_credits}", True, (255, 255, 255))
        screen.blit(credits_text, (400, 100))

        screen.blit(self.scrap_img, (350, 100))
        scraps_text = self.font.render(f"Scraps: {self.gained_scraps}", True, (255, 255, 255))
        screen.blit(scraps_text, (400, 150))

        self.continue_button.draw(screen)