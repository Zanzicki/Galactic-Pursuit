
import pygame
from Components.button import Button

class OptionsSettings:
    def __init__(self, sound_manager, game_world):
        self.sound_manager = sound_manager
        self.game_world = game_world
        screen_width = game_world.width

        font = pygame.font.Font(None, 36)

        self.music_up = Button(screen_width/2 - 100, 190, 250, 50, "Music Volume Up", (0, 255, 0), (0, 200, 0), (255, 255, 255), font)
        self.music_down = Button(screen_width/2 - 100, 260, 250, 50, "Music Volume Down", (0, 255, 0), (0, 200, 0), (255, 255, 255), font)
        self.sound_up = Button(screen_width/2 - 100, 330, 250, 50, "Sound Volume Up", (0, 255, 0), (0, 200, 0), (255, 255, 255), font)
        self.sound_down = Button(screen_width/2 - 100, 400, 250, 50, "Sound Volume Down", (0, 255, 0), (0, 200, 0), (255, 255, 255), font)
        self.back_button = Button(screen_width/2 - 100, 470, 250, 50, "Back", (255, 0, 0), (200, 0, 0), (255, 255, 255), font)

        self.buttons = [self.music_up, self.music_down, self.sound_up, self.sound_down, self.back_button]

    def handle_event(self, event):
        for button in self.buttons:
            if button.is_clicked(event):
                if button == self.music_up:
                    self.sound_manager.increase_music_volume()
                elif button == self.music_down:
                    self.sound_manager.decrease_music_volume()
                elif button == self.sound_up:
                    self.sound_manager.increase_sound_volume()
                elif button == self.sound_down:
                    self.sound_manager.decrease_sound_volume()
                elif button == self.back_button:
                    self.game_world._game_state = "menu"

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)
        font = pygame.font.Font(None, 36)
        music_text = font.render(f"Music Volume: {self.sound_manager.get_music_volume():.1f}", True, (255, 255, 255))
        sound_text = font.render(f"Sound Volume: {self.sound_manager.get_sound_volume():.1f}", True, (255, 255, 255))

        screen.blit(music_text, (300, 220))
        screen.blit(sound_text, (300, 400))

