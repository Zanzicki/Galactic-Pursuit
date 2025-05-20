import pygame


class UIElement():
    def __init__(self):
        self.font = pygame.font.Font("Assets/Fonts/ImpactfulBits.ttf", 24)

    def draw(self, text, position):
        ui_text = self.font.render(text, True, (255, 0, 0))
        self.screen.blit(ui_text, (position[0] - ui_text.get_width() // 2,
        position[1] // 2 - ui_text.get_height() // 2))