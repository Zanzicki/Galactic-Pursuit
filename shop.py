import pygame
import pygame_gui
import random
from Components import artifact, card
import upgrades


class Shop:
    def __init__(self, game_world):
        self.game_world = game_world
        self.screen = game_world.screen
        self.manager = pygame_gui.UIManager((1080, 720))
        self.background = pygame.Surface((1080, 720))
        self.background.fill(pygame.Color('#2e2e2e'))
        self.font = pygame.font.Font(None, 36)

        # Player setup
        self.player_gold = 50
        self.player_inventory = []

        # Sample items
        self.cards = ['Strike+', 'Defend+', 'Bash', 'Clash', 'Pommel Strike']
        self.potions = ['Strength Potion', 'Dexterity Potion', 'Health Potion']
        self.repair_ship = ['Repair your ship (heal 30% of max health)']
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
            'potions': random.sample(self.potions, 2),
            'repair': random.sample(self.repair_ship,1)
        }

        # UI elements
        self.buttons = []
        self.create_ui_elements()

    def create_ui_elements(self):
        """Create UI elements for shop items."""
        # Create buttons for cards
        for i, item in enumerate(self.shop_items['cards']):
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((50 + i * 200, 100), (180, 60)),
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


        for i, item in enumerate(self.shop_items['repair']):
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((50 + i * 200, 400), (320, 60)),
                text=f"{item} ({self.item_prices['repair']}g)",
                manager=self.manager
            )
            self.buttons.append(('repair', item, button))

        # Exit button
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((490, 500), (100, 50)),
            text='Exit',
            manager=self.manager
        )

    def run(self):
        """Run the shop interface."""
        clock = pygame.time.Clock()
        running = True
        while running:
            time_delta = clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_world._running = False
                    running = False

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
                        self.game_world._state = "map"
                        return

                self.manager.process_events(event)

            self.manager.update(time_delta)
            self.screen.blit(self.background, (0, 0))
            self.manager.draw_ui(self.screen)
            pygame.display.update()