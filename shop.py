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