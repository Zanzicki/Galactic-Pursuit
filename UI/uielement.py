import pygame
import pygame_gui


class UIElement():
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font("Assets/Fonts/ImpactfulBits.ttf", 24)

        self.credit_img = pygame.image.load("Assets/Icons/credit.png").convert_alpha()
        self.scrap_img = pygame.image.load("Assets/Icons/scrap.png").convert_alpha()

    def draw(self, text, position, credits, scraps, health, max_health, tmp_health=0):
        pygame.draw.rect(self.screen, (40,40,40),(0,0,1280,40))

        ui_text = self.font.render(text, True, (255, 0, 0))
        self.screen.blit(ui_text, (position[0] - ui_text.get_width() // 2,  
        position[1] // 2 - ui_text.get_height() // 2))

        # Draw credit icon and value
        self.screen.blit(self.credit_img, (20, 5))
        credits_text = self.font.render(f"{credits}", True, (255,215,0))
        self.screen.blit(credits_text, (60, 5))  

        # Draw scrap icon and value
        self.screen.blit(self.scrap_img, (140, 5))
        scraps_text = self.font.render(f"{scraps}", True, (192,192,192))
        self.screen.blit(scraps_text, (180, 5)) 

        if tmp_health > 0:
            health_text = self.font.render(f"Health: {health}/{max_health} (+{tmp_health})", True, (0,0,255))
            self.screen.blit(health_text, (1080,5))
        elif tmp_health <= 0:
            health_text = self.font.render(f"Health: {health}/{max_health}", True, (0,255,0))
            self.screen.blit(health_text, (1120,5))
    
    # Draws the health bar of a game object
    def draw_healthbar(self, screen, health, max_health, position):
        x, y = position
        bar_width = 200
        bar_height = 24
        health_percentage = min(health / max_health, 1.0)
        pygame.draw.rect(screen, (0, 255, 0), (x, y, int(bar_width * health_percentage), bar_height))
        # Draw overheal in blue
        if health > max_health:
            overheal_percentage = min((health - max_health) / max_health, 1.0)
            pygame.draw.rect(
                screen, (0, 128, 255),
                (x + int(bar_width * health_percentage), y, int(bar_width * overheal_percentage), bar_height)
            )
        # Draw health text (show actual health, even if overhealed)
        font = pygame.font.Font(None, 24)
        health_text = font.render(f"Health: {health}/{max_health}", True, (255, 255, 255))
        text_rect = health_text.get_rect(center=(x + bar_width // 2, y + bar_height // 2))
        screen.blit(health_text, text_rect)
    
    def draw_text(self, text, position, color=(255, 255, 255)):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=position)
        self.screen.blit(text_surface, text_rect)
