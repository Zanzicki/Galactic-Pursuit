import pygame
from Components.component import Component

class CardDisplay(Component):
    def __init__(self, card_data):
        super().__init__()
        self.card_data = card_data  # Reference to the Card data object
    
    def awake(self, game_world):
        pass

    def start(self):
        # Initialize any necessary data or state here
        pass
    def update(self, game_world):
        pass

    def draw_cardtext(self, screen, gameObject):
        # Use self.card_data for all display info
        font = pygame.font.Font("Assets/Fonts/ImpactfulBits.ttf", 15)
        text_surface = font.render(f"{self.card_data._name} \n{self.card_data._description}", True, (0,0,0))
        spriterenderer = gameObject.get_component("SpriteRenderer")
        if spriterenderer:
            sprite_rect = spriterenderer.sprite_image.get_rect(topleft=gameObject.transform.position)
            x = sprite_rect.x + (sprite_rect.width - text_surface.get_width()) // 1.5
            y = sprite_rect.y + (sprite_rect.height - text_surface.get_height()) // 1.5
            screen.blit(text_surface, (x, y))