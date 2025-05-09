import pygame
from Components.component import Component

# made by Erik

class CardHoverHandler(Component):  
    def __init__(self):
        super().__init__()
        self._hovered = False
        self.clicked = False
        self.font = pygame.font.Font(None, 36)

    def awake(self, game_world):
        self._game_world = game_world

    def start(self):
        pass

    def update(self, delta_time):
        # ✅ Local import to avoid circular dependency
        from gameworld import GameWorld

        sprite_renderer = self.gameObject.get_component("SpriteRenderer")
        if not sprite_renderer:
            return

        rect = sprite_renderer.sprite.rect 
        rect.topleft = self.gameObject.transform.position

        mouse_pos = pygame.mouse.get_pos()
        self._hovered = rect.collidepoint(mouse_pos)

        if self._hovered:
            pygame.draw.rect(self._game_world.screen, (255, 0, 0), rect, 2)

            card_info = self.gameObject.get_component("Card")
            if not card_info:
                return

            info_text = f"Name: {getattr(card_info, '_name', '???')} - rarity: {getattr(card_info, '_rarity', '???')} - value: {getattr(card_info, '_value', '???')}"
            description = f"Description: {getattr(card_info, '_description', '???')}"

            text_surface_1 = self.font.render(info_text, True, (255, 255, 255))
            text_surface_2 = self.font.render(description, True, (200, 200, 200))

             # Center the text in the middle of the screen
            screen_center = self._game_world.screen.get_rect().center
            text_x = screen_center[0] - (max(text_surface_1.get_width(), text_surface_2.get_width()) // 2)
            text_y = screen_center[1] - 100  # slightly above center

            text_bg_rect = pygame.Rect(
                text_x - 5,
                text_y - 5,
                max(text_surface_1.get_width(), text_surface_2.get_width()) + 10,
                60
            )
            pygame.draw.rect(self._game_world.screen, (0, 0, 0), text_bg_rect)
            pygame.draw.rect(self._game_world.screen, (255, 255, 255), text_bg_rect, 1)

            self._game_world.screen.blit(text_surface_1, (text_x, text_y))
            self._game_world.screen.blit(text_surface_2, (text_x, text_y + 25))
            
            if pygame.mouse.get_pressed()[0]:  # Left click
                if not self.clicked:
                 self.clicked = True
                 print(f"Card clicked!")
                 print(vars(card_info))
                 self.gameObject.is_destroyed = True
        else:
            self.clicked = False

