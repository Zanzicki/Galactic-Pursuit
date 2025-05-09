import pygame
import pygame_gui
from array import array
import random
import currency
import upgrades
from Components import artifact
from Components import card

screen_width = 1080
screen_height = 720

# Initialize Pygame and Pygame GUI
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Interstellar Trade Sector")
background = pygame.Surface((1080, 720))
background.fill(pygame.Color('#2e2e2e'))
manager = pygame_gui.UIManager((1080, 720))

# Sample items
cards = ['Strike+', 'Defend+', 'Bash', 'Clash', 'Pommel Strike']#card
available_upgrades = []

potions = ['Strength Potion', 'Dexterity Potion', 'Health Potion']#artifacts

# Prices
item_prices = {
    'card': 15,
    'upgrade': 20,
    'artifact': 25,
    'repair': 8
}

# Player setup
player_gold = 50
player_inventory = []

# Random shop generation
shop = {
    'cards': random.sample(cards, 3),
    'upgrade': random.sample(upgrades.selected_dictionaries,3),
    'potions': random.sample(potions, 2)
}

# Create UI elements for shop items
buttons = []
# for i, item in enumerate(shop['cards']):
#     button = pygame_gui.elements.UIButton(
#         relative_rect=pygame.Rect((50 + i * 200, 100), (180, 60)),
#         text=f"{item} ({item_prices['card']}g)",
#         manager=manager
#     )
#     buttons.append(('card', item, button))

for i, item in enumerate(shop['upgrade']):
    button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((50 + i * 200, 200), (180, 60)),
        text=f"{item} ({item_prices['upgrade']}g)",
        manager=manager
    )
    buttons.append(('upgrade', item, button))

# for i, item in enumerate(shop['potions']):
#     button = pygame_gui.elements.UIButton(
#         relative_rect=pygame.Rect((50 + i * 200, 300), (180, 60)),
#         text=f"{item} ({item_prices['potion']}g)",
#         manager=manager
#     )
#     buttons.append(('potion', item, button))

# Exit button
exit_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((490, 500), (100, 50)),
    text='Exit',
    manager=manager
)

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            for item_type, item_name, button in buttons:
                if event.ui_element == button:
                    item_cost = item_prices[item_type]
                    if player_gold >= item_cost:
                        player_gold -= item_cost
                        player_inventory.append(item_name)
                        print(f"Bought {item_name} for {item_cost} gold.")
                    else:
                        print("Not enough gold.")
            if event.ui_element == exit_button:
                running = False

        manager.process_events(event)

    manager.update(time_delta)
    screen.blit(background, (0, 0))
    manager.draw_ui(screen)
    pygame.display.update()

pygame.quit()

class Shop:
    def __init__(self, game_world):
        self.game_world = game_world
        self.screen = game_world.screen
        self.font = pygame.font.Font(None, 36)
        self.items = self.generate_shop_items()
        self.selected_item_index = 0  # Track the currently selected item
        self.player_gold = 100  # Example player gold

    def generate_shop_items(self):
        return [
            {"name": "Health Potion", "price": 10},
            {"name": "Strength Potion", "price": 15},
            {"name": "Dexterity Potion", "price": 20},
            {"name": "Repair Kit", "price": 25},
        ]

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_world._running = False
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print("Returning to map!")
                        self.game_world._state = "map"  # Transition back to map state
                        return
                    elif event.key == pygame.K_UP:
                        self.selected_item_index = (self.selected_item_index - 1) % len(self.items)
                    elif event.key == pygame.K_DOWN:
                        self.selected_item_index = (self.selected_item_index + 1) % len(self.items)
                    elif event.key == pygame.K_RETURN:
                        self.purchase_item()

            # Draw the shop screen
            self.screen.fill((50, 50, 50))
            self.draw_shop()
            pygame.display.flip()

    def draw_shop(self):
        title_surface = self.font.render("Welcome to the Shop!", True, (255, 255, 255))
        self.screen.blit(title_surface, (self.game_world.width // 2 - title_surface.get_width() // 2, 50))

        gold_surface = self.font.render(f"Gold: {self.player_gold}", True, (255, 255, 0))
        self.screen.blit(gold_surface, (50, 50))

        for i, item in enumerate(self.items):
            color = (255, 255, 255) if i == self.selected_item_index else (200, 200, 200)
            item_surface = self.font.render(f"{item['name']} - {item['price']} Gold", True, color)
            self.screen.blit(item_surface, (50, 150 + i * 40))

    def purchase_item(self):
        selected_item = self.items[self.selected_item_index]
        if self.player_gold >= selected_item["price"]:
            self.player_gold -= selected_item["price"]
            print(f"Purchased {selected_item['name']} for {selected_item['price']} gold!")
        else:
            print(f"Not enough gold to purchase {selected_item['name']}!")