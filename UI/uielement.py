import pygame
import pygame_gui


class UIElement():
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font("Assets/Fonts/ImpactfulBits.ttf", 24)

    def draw(self, text, position, gold, scrap):
        pygame.draw.rect(self.screen, (40,40,40),(0,0,1280,40))

        # round_rendered = self.font.render(text, True, (255, 0, 0))
        # self.screen.blit(
        #     round_rendered,
        #     (540 - round_rendered.get_width() // 2, 25 - round_rendered.get_height() // 2)
        # )
        ui_text = self.font.render(text, True, (255, 0, 0))
        self.screen.blit(ui_text, (position[0] - ui_text.get_width() // 2,
        position[1] // 2 - ui_text.get_height() // 2))

        gold_text = self.font.render(f"Gold: {gold}", True, (255,215,0))
        self.screen.blit(gold_text, (20,5))

        scrap_text = self.font.render(f"Scrap: {scrap}", True, (192,192,192))
        self.screen.blit(scrap_text, (200,5))