import pygame
from Components.button import Button

class UIManager:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.buttons = []

    def set_buttons(self, button_configs):
        self.buttons = []
        for config in button_configs:
            button = Button(
                x=config["x"],
                y=config["y"],
                width=config["width"],
                height=config["height"],
                text=config["text"],
                color=(0, 200, 255),
                hover_color=(0, 255, 255),
                text_color=(255, 255, 255),
                font=self.font
            )
            button.action = config.get("action")  # Attach the action to the button
            self.buttons.append(button)

    def draw(self, screen):
        for button in self.buttons:
            button.draw(screen)

    def handle_event(self, event):
        for button in self.buttons:
            if button.is_clicked(event) and hasattr(button, "action"):
                button.action()

    def draw_card_screen(self, screen):
        self.draw(screen)  # Reuse the draw method to draw buttons


    
        
        