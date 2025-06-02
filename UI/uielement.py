import pygame
import pygame_gui


class UIElement():
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font("Assets/Fonts/ImpactfulBits.ttf", 24)

    def draw(self, text, position, gold, scrap, health, max_health):
        pygame.draw.rect(self.screen, (40,40,40),(0,0,1280,40))

        ui_text = self.font.render(text, True, (255, 0, 0))
        self.screen.blit(ui_text, (position[0] - ui_text.get_width() // 2,
        position[1] // 2 - ui_text.get_height() // 2))

        gold_text = self.font.render(f"Gold: {gold}", True, (255,215,0))
        self.screen.blit(gold_text, (20,5))

        scrap_text = self.font.render(f"Scrap: {scrap}", True, (192,192,192))
        self.screen.blit(scrap_text, (200,5))

        health_text = self.font.render(f"Health: {health}/{max_health}", True, (0,255,0))
        self.screen.blit(health_text, (1120,5))
    
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
