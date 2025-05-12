from abc import ABC, abstractmethod
import pygame

# Base class for all components
class Component(ABC):

    def __init__(self) -> None:
        super().__init__()
        self._gameObject = None

    @property
    def gameObject(self):
        return self._gameObject
    
    @gameObject.setter
    def gameObject(self,value):
        self._gameObject = value

    @abstractmethod
    def awake(self, game_world):
        pass
    
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def update(self, delta_time):
        pass

# Transform component to handle position and movement
class Transform(Component):

    def __init__(self, position) -> None:
        super().__init__()
        self._position = position

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self,value):
        self._position = value

    def translate(self, direction):
        self._position += direction

    @property
    def flip(self):
        return self._flip

    def awake(self, game_world):
        pass

    def start(self):
        pass
   
    def update(self, delta_time):
        pass 

# SpriteRenderer component to handle rendering of sprites
class SpriteRenderer(Component):

    def __init__(self, sprite_name) -> None:
        super().__init__()

        self._sprite_image = pygame.image.load(f"Assets\\{sprite_name}") # Load sprite image
        self._sprite_name = sprite_name
        self._sprite = pygame.sprite.Sprite()
        self._sprite.rect = self._sprite_image.get_rect()
        self._sprite_mask = pygame.mask.from_surface(self.sprite_image)

    @property
    def sprite_image(self):
        return self._sprite_image
    
    @property
    def sprite_mask(self):
        return self._sprite_mask
    
    @sprite_image.setter
    def sprite_image(self, value):
        self._sprite_image= value

    @property
    def sprite(self):
        return self._sprite
    
    @property
    def sprite_name(self):
        return self._sprite_name
    
    def awake(self, game_world, ):
      self._game_world = game_world
      self._sprite.rect.topleft = self.gameObject.transform.position

    def set_offset(self, x_offset, y_offset):
        self._sprite.rect.x += x_offset
        self._sprite.rect.y += y_offset

    def start(self):
        pass
   
    def update(self, delta_time):
        self._sprite.rect.topleft = self.gameObject.transform.position
        self._game_world.screen.blit(self._sprite_image,self._sprite.rect) 

# Animator component to handle animations
class Animator(Component):

    def __init__(self) -> None:
        super().__init__()
        self._animations = {}
        self._current_animation = None
        self._animation_time = 0
        self._current_frame_index = 0

    def add_animation(self, name, *args):
        frames = []
        for arg in args:
            #sprite_image = pygame.image.load(f"Assets\\{arg}")
            sprite_image = pygame.image.load(f"Assets\\{arg}") # Load each frame
            frames.append(sprite_image)
        
        self._animations[name] = frames

    def add_spritesheet_animation(self, name, spritesheet_path, frame_width, frame_height, frame_count):
        spritesheet = pygame.image.load(spritesheet_path)
        frames = []
        for i in range(frame_count):
            frame_rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
            frame_image = spritesheet.subsurface(frame_rect)
            frames.append(frame_image)
        
        self._animations[name] = frames

    def play_animation(self, animation):
        self._current_animation = animation
        self._current_frame_index = 0  # Reset frame index when playing a new animation

    def awake(self, game_world):
        self._sprite_renderer = self._gameObject.get_component("SpriteRenderer")
    
    def start(self):
        pass

    def update(self, delta_time):
        frame_duration = 0.1
        self._animation_time += delta_time

        if self._animation_time >= frame_duration:
            self._animation_time = 0
            self._current_frame_index += 1
            
            animation_sequence = self._animations[self._current_animation]

            if self._current_frame_index >= len(animation_sequence):
                self._current_frame_index = 0  # Reset animation
            
            self._sprite_renderer.sprite_image = animation_sequence[self._current_frame_index]
            
    def add_spritesheet_animation(self, name, spritesheet_path, frame_width, frame_height, frame_count):
            spritesheet = pygame.image.load(spritesheet_path)
            frames = []
            for i in range(frame_count):
                frame_rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
                frame_image = spritesheet.subsurface(frame_rect)
                frames.append(frame_image)

            self._animations[name] = frames