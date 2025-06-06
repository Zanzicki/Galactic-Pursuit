import pygame
import pygame_gui
from BuilderPattern.playerbuilder import PlayerBuilder
from Components import player
from Components.player import Player
from GameState.map import Map
from gameobject import GameObject
from soundmanager import SoundManager


class EndGameScreen:
    def __init__(self, game_world):
        self.game_world = game_world
        self.ui_manager = pygame_gui.UIManager((game_world.width, game_world.height))
        self.font = pygame.font.Font(None, 36)
        self.player = Player()
        self.restart_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((game_world.width // 2 - 50, game_world.height // 3 - 25), (100, 50)),
            text='Restart',
            manager=self.ui_manager
        )

    def restart_game(self):
    # Ryd gameObjects
        
        self.game_world._gameObjects.clear()
        #genskab menu
        
        self.game_world._game_state  = "menu"
        self.game_world.ui_manager.show_menu_buttons()
        self.game_world.ui_manager.back_to_map_button.hide()
        self.restart_player()        
        SoundManager().fade_in_music("Assets/SoundsFiles/backgroundmusiclooped.mp3", loop=True, fade_time_ms=3000)

    # depending on the palyers health write and message on the end screen
    def get_player_status_alive_or_dead(self):
        return "You Saved the galaxy" if self.player.health > 0 else "Game over you are dead"

    def update(self, time_delta, events):
        for event in events:
            self.ui_manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.restart_button:
                    self.restart_game()
                    self.game_world._game_state  ="menu"
                                        
                    print("Restarting game...")
        SoundManager().fade_out_music(5000)
        
        self.ui_manager.update(time_delta)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        status_text = self.font.render(f"{self.get_player_status_alive_or_dead()}", True, (255, 255, 255))
        screen.blit(status_text, (self.game_world.width // 2 - status_text.get_width() // 2, self.game_world.height // 2))
        self.ui_manager.draw_ui(screen)

    def restart_player(self):
        builder = PlayerBuilder()
        builder.build()
        self.game_world.playerGo = builder.get_gameObject()
        self.game_world.player = builder.player
        Player._instance = self.game_world.player
        self.game_world.instantiate(self.game_world.playerGo)