from Components.component import Component
import pygame

from Components.player import Player

class Planet(Component):
    def __init__(self, name, size, color, position, gameworld):
        super().__init__()
        self._name = name
        self._size = size
        self._color = color
        self._position = position
        self._highlighted = False  # Whether the planet is highlighted
        self.font = pygame.font.Font(None, 24)  # Font for rendering text
        self._gameworld = gameworld
        self._visited = False  # Track if the planet has been visited
        self.player = Player.get_instance()

    @property
    def name(self):
        return self._name

    @property
    def size(self):
        return self._size

    @property
    def color(self):
        return self._color

    @property
    def position(self):
        return self._position
    
    @property
    def visited(self):
        return self._visited
    
    @visited.setter
    def visited(self, value):
        self._visited = value

    def awake(self, game_world):
        pass

    def start(self):
        pass

    def update(self, delta_time):
        player_pos= self._gameworld.get_player_position()

        if player_pos is None:
            return
        
        # Check if the planet is close to the player
        dx = player_pos[0] - self._position[0]
        dy = player_pos[1] - self._position[1]
        distance = (dx ** 2 + dy ** 2) ** 0.5
        self._highlighted = distance <= self._size + 20

    def draw(self, screen, font):

        color = (100, 100, 100) if self._visited == True else self._color
        # Draw the planet
        pygame.draw.circle(screen, color, self._position, self._size)
         
            
        # Draw highlight if the planet is close to the player
        if self._highlighted and self._visited == False:
            pygame.draw.circle(screen, (255, 255, 255), self._position, self._size + 5, 2)
            text_surface = font.render(self._name, True, (255, 255, 255))
            screen.blit(text_surface, (self._position[0] - 20, self._position[1] - 40))