import pygame
import pygame_gui

class OptionsSettings:
    def __init__(self, sound_manager, game_world):
        self.sound_manager = sound_manager
        self.game_world = game_world
        self.manager = game_world.ui_manager.ui_manager
        self.screen_width = game_world.width
        self.buttons_created = False

    def enter(self):
        if not self.buttons_created:
            # Create pygame_gui buttons
            self.music_up = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((self.screen_width//2 - 100, 190), (250, 50)),
                text="Music Volume Up",
                manager=self.manager
            )
            self.music_down = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((self.screen_width//2 - 100, 260), (250, 50)),
                text="Music Volume Down",
                manager=self.manager
            )
            self.sound_up = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((self.screen_width//2 - 100, 330), (250, 50)),
                text="Sound Volume Up",
                manager=self.manager
            )
            self.sound_down = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((self.screen_width//2 - 100, 400), (250, 50)),
                text="Sound Volume Down",
                manager=self.manager
            )
            self.back_button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((self.screen_width//2 - 100, 470), (250, 50)),
                text="Back",
                manager=self.manager
            )

            self.buttons = [
                self.music_up, self.music_down, self.sound_up, self.sound_down, self.back_button
            ]
            self.buttons_created = True

    def handle_event(self, events):
        for event in events:
            self.manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.music_up:
                    self.sound_manager.increase_music_volume()
                elif event.ui_element == self.music_down:
                    self.sound_manager.decrease_music_volume()
                elif event.ui_element == self.sound_up:
                    self.sound_manager.increase_sound_volume()
                elif event.ui_element == self.sound_down:
                    self.sound_manager.decrease_sound_volume()
                elif event.ui_element == self.back_button:
                    for button in self.buttons:
                        button.kill()
                    self.buttons_created = False
                    self.game_world._game_state = "menu"

    def draw(self, screen, delta_time):
        self.manager.update(delta_time)
        self.manager.draw_ui(screen)
        font = pygame.font.Font(None, 36)
        music_text = font.render(f"Music Volume: {self.sound_manager.get_music_volume():.1f}", True, (255, 255, 255))
        sound_text = font.render(f"Sound Volume: {self.sound_manager.get_sound_volume():.1f}", True, (255, 255, 255))
        screen.blit(music_text, (300, 220))
        screen.blit(sound_text, (300, 400))

