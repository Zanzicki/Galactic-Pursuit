import random
import pygame

class HitEffect:
    def __init__(self):
        self.hit_timer = 0
        self.shake_offset = (0, 0)
        self.damage_popup = None
        self.damage_popup_timer = 0
        self.is_hit_animating = False  # <-- Add this flag

    def trigger_hit(self, damage, shake_time=0.15, popup_time=0.7):
        self.hit_timer = shake_time
        self.shake_offset = (0, 0)
        self.damage_popup = damage
        self.damage_popup_timer = popup_time
        self.is_hit_animating = True  # <-- Set flag when hit

    def update_hit_effect(self, delta_time):
        if self.hit_timer > 0:
            self.hit_timer -= delta_time
            self.shake_offset = (random.randint(-8, 8), random.randint(-8, 8))
        else:
            self.shake_offset = (0, 0)
            self.is_hit_animating = False  # <-- Unset flag when done
        if self.damage_popup_timer > 0:
            self.damage_popup_timer -= delta_time
            if self.damage_popup_timer <= 0:
                self.damage_popup = None

    def draw_hit_effect(self, screen, sprite_image, position):
        pos = (position[0] + self.shake_offset[0], position[1] + self.shake_offset[1])
        # Flash white if hit
        if self.hit_timer > 0:
            white_sprite = sprite_image.copy()
            white_sprite.fill((255,255,255), special_flags=pygame.BLEND_RGB_ADD)
            screen.blit(white_sprite, pos)
        else:
            screen.blit(sprite_image, pos)
        # Draw damage popup
        if self.damage_popup is not None:
            font = pygame.font.Font(None, 48)
            dmg_text = font.render(f"-{self.damage_popup}", True, (255, 0, 0))
            sprite_rect = sprite_image.get_rect(topleft=pos)
            popup_x = sprite_rect.centerx - dmg_text.get_width() // 2
            popup_y = sprite_rect.centery - dmg_text.get_height() // 2
            screen.blit(dmg_text, (popup_x, popup_y))