import pygame
import pygame_gui
from BuilderPattern.playerbuilder import PlayerBuilder
from Components.player import Player
from map import Map
from gameobject import GameObject
from menu import Menu
class EndGameScreen:
    def __init__(self, game_world):
        self.game_world = game_world
        self.ui_manager = pygame_gui.UIManager((game_world.width, game_world.height))
        self.font = pygame.font.Font(None, 36)
        
        self.restart_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((game_world.width // 2 - 50, game_world.height // 4 - 25), (100, 50)),
            text='Restart',
            manager=self.ui_manager
        )
    
    def restart_game(self):
    # Ryd gameObjects
        self.game_world._gameObjects.clear()
        #genskab menu
        
        self.game_world.state = "menu"
        self.game_world.ui_manager.play_button.show()
        self.game_world.ui_manager.options_button.show()
        self.game_world.ui_manager.quit_button.show()

    # Rebuild player
        builder = PlayerBuilder()
        builder.build()
        player = Player.get_instance()
        self.game_world._gameObjects.append(builder.get_gameObject())
        builder.get_gameObject().transform.position = pygame.math.Vector2(
        self.game_world.width // 2, self.game_world.height // 2
    )
        self.game_world.player = player

        
       
    # Reset kort og tilstande
        self.game_world._deck.cards.clear()
        self.game_world._create_card = False

    # Genskab map
        self.game_world.map = Map(self.game_world)
        self.game_world.map.generate_planets()
        
         # After all game objects are created and added to self.game_world._gameObjects
        for game_object in self.game_world._gameObjects:
            for component in game_object._components.values():
                    component._game_world = self.game_world
                    print(f"Set _game_world for {component}")


    def update(self, time_delta, events):
        for event in events:
            self.ui_manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.restart_button:
                    self.restart_game()
                    self.game_world.state ="menu"
                    print("Restarting game...")
        self.ui_manager.update(time_delta)

    def draw(self, screen):
        screen.fill((0, 0, 0))
        text = self.font.render("Game Over", True, (255, 0, 0))
        screen.blit(text, (self.game_world.width // 2 - text.get_width() // 2, self.game_world.height // 4 - text.get_height() // 2))
        self.ui_manager.draw_ui(screen)