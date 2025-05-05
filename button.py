import pygame

#Klasse til at tegne alle knapper, constructer til oprettelse af lister af knapper i UI Manager
#Bliver også brugt til at tjekke om de bliver trykket på
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_color = text_color
        self.font = font

#Tegner alle knapper og tjekker mouse pos
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        # Check if mouse is at button
        if self.rect.collidepoint(mouse_pos):
            color = self.hover_color
        else:
            color = self.color

        #Tegn knap
        pygame.draw.rect(screen, color, self.rect)

        text_surface = self.font.render(self.text, True, self.text_color)

        text_rect = text_surface.get_rect(center=self.rect.center)

        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True

        return False
