import pygame
from Components.button import Button

class UIManager:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(UIManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    
    #Constructoren opretter de forskellige lister af knapper, som skal vises alt efter hvilken skærm der vises
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

    def draw_options(self, screen):
        for button in self.options_buttons:
            button.draw(screen)

        options_lines =[
            "These are the options",
            "Change your gamma and whatever",
            "You can also change volume",
            "When we feel like adding it"
        ]
        y = 350

        for line in options_lines:
            options_text = self.font.render(line, True, (255,255,255))
            text_rect = options_text.get_rect(topleft=(10, y))
            screen.blit(options_text, text_rect)
            y += 30
    def draw_back_button(self, screen):
        self.back_button.draw(screen)
#Alle handle_event metoder står for at køre relevante funktioner alt efter hvilke knapper der trykkes på
    def handle_event(self, event):
        for button in self.buttons:
            if button.is_clicked(event) and hasattr(button, "action"):
                button.action()

    def draw_card_screen(self, screen):
        self.draw(screen)  # Reuse the draw method to draw buttons
