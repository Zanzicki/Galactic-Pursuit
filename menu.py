import pygame
from Components.button import Button
from UIManager import UIManager

#Denne fil står for tre klasser: Menu, EndGameMenu og Options.
#Hver klasse er en singleton og har hver deres run og constructor til at tegne hver deres skærm med relevant info
class Menu:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Menu, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            pygame.init()  # Ensure pygame is initialized here
            self.screen = pygame.display.set_mode((720, 500))
            self.running = True
            self.initialized = True

    def run(self):
        while self.running:
            self.screen.fill((30, 30, 30))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                UIManager().handle_event(event)

            UIManager().draw(self.screen)
            pygame.display.flip()

        pygame.quit()


class EndGameMenu:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(EndGameMenu, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            pygame.init()
            self.screen = pygame.display.set_mode((400,300))
            self.font = pygame.font.Font(None, 36)
            self.running = True
            self._initialized = True

    def run(self):
        while self.running:
                self.screen.fill((50, 50, 50))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    UIManager().handle_endgame(event)

                UIManager().draw_end_screen(self.screen)
                pygame.display.flip()

class Options:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Options, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            pygame.init()
            self.screen = pygame.display.set_mode((800,600))
            self.font = pygame.font.Font(None, 36)
            self.running = True
            self._initialized = True

    def run(self):
        while self.running:
                self.screen.fill((50, 50, 50))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    UIManager().handle_options(event)

                UIManager().draw_options(self.screen)
                pygame.display.flip()
