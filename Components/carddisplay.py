import pygame
from Components.component import Component
from Components.card import Card

class CardDisplay(Component):
    def __init__(self, card_data):
        super().__init__()
        # Always store a Card object
        if isinstance(card_data, tuple):
            card_data = Card(*card_data[1:7])
        self.card_data = card_data  # Reference to the Card data object
    
    def awake(self, game_world):
        pass

    def start(self):
        # Initialize any necessary data or state here
        pass
    def update(self, game_world):
        pass

    def draw_cardtext(self, screen, gameObject):
        font = pygame.font.Font("Assets/Fonts/ImpactfulBits.ttf", 15)
        card = self.card_data
        text_surface = font.render(f"{card._name} \n{card._description}", True, (0,0,0))
        spriterenderer = gameObject.get_component("SpriteRenderer")
        if spriterenderer:
            sprite_rect = spriterenderer.sprite_image.get_rect(topleft=gameObject.transform.position)
            x = sprite_rect.x + (sprite_rect.width - text_surface.get_width()) // 1.5
            y = sprite_rect.y + (sprite_rect.height - text_surface.get_height()) // 1.5
            screen.blit(text_surface, (x, y))