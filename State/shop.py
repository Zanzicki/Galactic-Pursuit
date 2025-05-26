import pygame
import random

import pygame_gui
from Components import artifact, card
import upgrades

class Shop:
    _instance = None

    def __init__(self, game_world):
        if Shop._instance is not None:
            raise Exception("Shop is a singleton! Use Shop.get_instance().")
        Shop._instance = self
        self.game_world = game_world
        self.screen = game_world.screen
        self.manager = game_world.ui_manager.ui_manager  # Use the shared UIManager
        self.background = pygame.Surface((self.screen.get_size()))
        self.background.fill(pygame.Color('#2e2e2e'))
        self.font = pygame.font.Font(None, 36)

        # Player setup
        self.player_gold = 50
        self.player_inventory = []

        # Sample items
        self.cards = ['Strike+', 'Defend+', 'Bash', 'Clash', 'Pommel Strike']
        self.potions = ['Strength Potion', 'Dexterity Potion', 'Health Potion']
        self.item_prices = {
            'card': 15,
            'upgrade': 20,
            'artifact': 25,
            'repair': 8
        }

        # Random shop generation
        self.shop_items = {
            'cards': random.sample(self.cards, 3),
            'upgrade': random.sample(upgrades.selected_dictionaries, 3),
            'potions': random.sample(self.potions, 2)
        }

        # UI elements
        self.buttons = []

    @staticmethod
    def get_instance():
        if Shop._instance is None:
            raise Exception("Shop has not been initialized! Call Shop(game_world) first.")
        return Shop._instance

    def create_ui_elements(self):
        self.buttons.clear()
        # Create buttons for cards
        for i, item in enumerate(self.shop_items['cards']):
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((50 + i * 200, 100), (-1, -1)),
                text=f"{item} ({self.item_prices['card']}g)",
                manager=self.manager
            )
            self.buttons.append(('card', item, button))

        # Create buttons for upgrades
        for i, item in enumerate(self.shop_items['upgrade']):
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((50 + i * 200, 200), (180, 60)),
                text=f"{item} ({self.item_prices['upgrade']}g)",
                manager=self.manager
            )
            self.buttons.append(('upgrade', item, button))

        # Create buttons for potions
        for i, item in enumerate(self.shop_items['potions']):
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((50 + i * 200, 300), (180, 60)),
                text=f"{item} ({self.item_prices['artifact']}g)",
                manager=self.manager
            )
            self.buttons.append(('artifact', item, button))

        # Exit button
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((490, 500), (100, 50)),
            text='Exit',
            manager=self.manager
        )

    def enter(self):
        self.create_ui_elements()  # Create buttons when entering shop

    def exit(self):
        # Destroy all shop buttons when leaving shop
        for _, _, button in self.buttons:
            button.kill()
        self.exit_button.kill()
        self.buttons.clear()

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            for item_type, item_name, button in self.buttons:
                if event.ui_element == button:
                    item_cost = self.item_prices[item_type]
                    if self.player_gold >= item_cost:
                        self.player_gold -= item_cost
                        self.player_inventory.append(item_name)
                        print(f"Bought {item_name} for {item_cost} gold.")
                    else:
                        print("Not enough gold.")
            if event.ui_element == self.exit_button:
                print("Returning to map!")
                self.game_world.state_changed_to_shop = "out"

        # Let the shared UIManager process the event
        self.manager.process_events(event)

    def update(self, delta_time):
        self.manager.update(delta_time)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.manager.draw_ui(self.screen)