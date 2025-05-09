import pygame
from Components.component import Component
from Components.card import Card
# mad by Erik

class CardHoverHandler(Component):  
    def __init__(self):
        super().__init__()
        self._hovered = False
        self.clicked = False
        self.font = pygame.font.Font(None, 36)  # Example font, adjust as needed

    def awake(self, game_world):
        self._game_world = game_world

    def start(self):
        pass

    def update(self, delta_time):
        sprite_renderer = self.gameObject.get_component("SpriteRenderer")
        card_component = self.gameObject.get_component("Card")
        if not sprite_renderer:
            return
        
        rect = sprite_renderer.sprite.rect 
        rect.topleft = self.gameObject.transform.position

        mouse_pos = pygame.mouse.get_pos()
        self._hovered = rect.collidepoint(mouse_pos)

        if self._hovered:
             pygame.draw.rect(self._game_world.screen, (255, 0, 0), rect, 2)

            # show card details on hover
             info_text = f"{card_component.name} - {card_component.rarity}"
             description = f"{card_component.description}"

             text_surface_1 = self.font.render(info_text, True, (255, 255, 255))
             text_surface_2 = self.font.render(description, True, (200, 200, 200))

            # Background box for text
             text_bg_rect = pygame.Rect(mouse_pos[0], mouse_pos[1], max(text_surface_1.get_width(), text_surface_2.get_width()) + 10, 40)
             pygame.draw.rect(self._game_world.screen, (0, 0, 0), text_bg_rect)
             pygame.draw.rect(self._game_world.screen, (255, 255, 255), text_bg_rect, 1)

            # Draw text on top of the background box
             self._game_world.screen.blit(text_surface_1, (mouse_pos[0] + 5, mouse_pos[1] + 2))
             self._game_world.screen.blit(text_surface_2, (mouse_pos[0] + 5, mouse_pos[1] + 20))


             if pygame.mouse.get_pressed()[0]:  # Left mouse button
                if not self.clicked:
                    self.clicked = True
                    # Add logic to handle card click, e.g., show card details or perform an action
                    print(f"Card {card_component.name} clicked!") # skal have tilføjet hvilken card der er trykket på
                    self.gameObject.is_destroyed = True  # Example action: destroy the card

        else:
            self.clicked = False
            # Add logic to remove card details or unhighlight the card
            
                