import pygame
import random
import pygame_gui
from Components.artifact import Artifact
from Components.card import Card
from Components.player import Player
from FactoryPatterns.artifactFactory import ArtifactFactory
from UI.uielement import UIElement
import upgrades
from Database.sqlrepository import SQLRepository

class Shop:
    _instance = None

    def __init__(self, game_world):
        if Shop._instance is not None:
            raise Exception("Shop is a singleton! Use Shop.get_instance().")
        Shop._instance = self
        self._game_world = game_world
        self.screen = game_world.screen
        self.manager = game_world.ui_manager.ui_manager
        self.background = pygame.Surface((self.screen.get_size()))
        self.background.fill(pygame.Color('#2e2e2e'))
        self.font = pygame.font.Font(None, 36)
        self.ui_element = UIElement(self.screen)
        self.player = Player.get_instance()
        self.repository = SQLRepository()
        self.artifact_factory = ArtifactFactory()

        # Prices
        self.item_gold_prices = {
            'card': 15,
            'artifact': 25
        }
        self.item_scrap_prices = {
            'upgrade': 20,
            'repair': 8
        }

        # Generate shop items from database
        self.generate_shop_items()

        # UI elements
        self.buttons = []

    # -------------------- Shop Inventory Generation --------------------
    def generate_shop_items(self):
        # Example column names, adjust as needed
        all_cards = [
            dict(zip(['id', 'name', 'value', 'type', 'rarity', 'description', 'price'], card))
            for card in self.repository.fetch_all_non_basic_cards()
        ]
        cards = random.sample(all_cards, min(2, len(all_cards)))
        all_artifacts = [
            dict(zip(['id', 'name', 'rarity', 'description', 'price'], artifact))
            for artifact in self.repository.fetch_all_artifacts()
        ]
        artifacts = random.sample(all_artifacts, min(2, len(all_artifacts)))
        self.shop_cards = cards
        self.shop_artifacts = artifacts

    # -------------------- UI Creation --------------------
    def create_ui_elements(self):
        self.buttons.clear()
        screen_width = 1280
        button_width = 220
        button_height = 60
        spacing = 60  # space between buttons

        # Center the two card buttons
        total_width = 2 * button_width + spacing
        start_x = (screen_width - total_width) // 2

        # Cards (credits)
        for i, card in enumerate(self.shop_cards):
            x = start_x + i * (button_width + spacing)
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((x, 200), (button_width, button_height)),
                text=card['name'],
                manager=self.manager
            )
            self.buttons.append(('card', card, button))

        # Center the two artifact buttons below cards
        for i, artifact in enumerate(self.shop_artifacts):
            x = start_x + i * (button_width + spacing)
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((x, 350), (button_width, button_height)),
                text=artifact['name'],
                manager=self.manager
            )
            self.buttons.append(('artifact', artifact, button))

        # Center the repair button below artifacts
        repair_x = (screen_width - button_width) // 2
        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((repair_x, 500), (button_width, button_height)),
            text="Repair Ship",
            manager=self.manager
        )
        self.buttons.append(('repair', None, button))

    def enter(self):
        self.create_ui_elements()

    def exit(self):
        for _, _, button in self.buttons:
            button.kill()
        if hasattr(self, "exit_button"):
            self.exit_button.kill()
        self.buttons.clear()

    # -------------------- Event Handling --------------------
    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            for item_type, item_data, button in self.buttons:
                if event.ui_element == button:
                    if item_type == 'card':
                        self.buy_card(item_data)
                    elif item_type == 'artifact':
                        self.buy_artifact(item_data)
                    elif item_type == 'repair':
                        self.handle_repair()
        self.manager.process_events(event)

    # -------------------- Card Service --------------------
    def buy_card(self, card_data):
        price = card_data['price']
        if self.player._credits >= price:
            self.player._credits -= price
            # Add card to player's deck in memory
            
            self.player.deck.add_card(Card(card_data['name'], card_data['value'], card_data['type'],card_data['rarity'],card_data['description'],card_data['price'] ))
            # Save to database
            self.repository.insert_player_card(self.player._id, card_data['id'])
            self.repository.update_player_currency(player_id=self.player._id, credits=self.player._credits)
            print(f"Bought {card_data['name']} for {price} credits.")
        else:
            print("Not enough credits.")

    # -------------------- Artifact Service --------------------
    def buy_artifact(self, artifact_data):
        price = artifact_data['price']
        if self.player._credits >= price:
            self.player._credits -= price
            # Add artifact to player in memory            # Save to database
            self.repository.insert_player_artifact(self.player._id, artifact_data['id'])
            self.repository.update_player_currency(player_id=self.player._id, credits=self.player._credits)
            artifact_go = self.artifact_factory.create_component(artifact_data)
            self._game_world.instantiate(artifact_go)
            self.player.artifacts.append(artifact_go)
            self.player.update_artifacts()

            print(f"Bought {artifact_data['name']} for {price} credits.")
        else:
            print("Not enough credits.")

    # -------------------- Repair Service --------------------
    def handle_repair(self):
        price = 15
        if self.player._scraps >= price:
            self.player._scraps -= price
            self.heal_player()
            self.repository.update_player_currency(player_id=self.player._id, scrap=self.player._scraps)
            print("Player healed!")
        else:
            print("Not enough scrap for repair.")

    def heal_player(self):
        heal_amount = 10
        self.player.health = min(self.player.health + heal_amount, self.player.max_health)

    # -------------------- Update & Draw --------------------
    def update(self, delta_time):
        self.manager.update(delta_time)

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        self.manager.draw_ui(self.screen)
        # Draw icons next to buttons
        for i, (_, card, button) in enumerate(self.buttons):
            if card and 'price' in card:
                # Draw credit icon next to card/artifact buttons
                self.ui_element.screen.blit(self.ui_element.credit_img, (button.relative_rect.x + button.relative_rect.width + 10, button.relative_rect.y + 10))
            elif _ == 'repair':
                self.ui_element.screen.blit(self.ui_element.scrap_img, (button.relative_rect.x + button.relative_rect.width + 10, button.relative_rect.y + 10))
        self.ui_element.draw("Intergalactic Trade Sector", (640, 40), self.player._credits, self.player._scraps, self.player._health, self.player._max_health)
    
    def draw_shop_prices_and_descriptions(self, screen, font):
        # Draw descriptions and prices for each button
        for item_type, item, button in self.buttons:
            bx, by = button.relative_rect.x, button.relative_rect.y
            bw, bh = button.relative_rect.width, button.relative_rect.height

            # Draw description under the button (if card or artifact)
            if item_type in ('card', 'artifact') and item:
                desc = item.get('description', '')
                if desc:
                    desc_surf = font.render(desc, True, (200, 200, 200))
                    desc_rect = desc_surf.get_rect(center=(bx + bw // 2, by + bh + 25))
                    self.screen.blit(desc_surf, desc_rect)

            # Draw price icon and number under the button
            if item_type == 'card' and item:
                price = item['price']
                icon = self.ui_element.credit_img
            elif item_type == 'artifact' and item:
                price = item['price']
                icon = self.ui_element.credit_img
            elif item_type == 'repair':
                price = 15
                icon = self.ui_element.scrap_img
            else:
                continue

            icon_y = by + bh + 45
            icon_x = bx + bw // 2 - 30
            self.screen.blit(icon, (icon_x, icon_y))
            price_surf = font.render(str(price), True, (255, 255, 255))
            price_rect = price_surf.get_rect(midleft=(icon_x + icon.get_width() + 8, icon_y + icon.get_height() // 2))
            self.screen.blit(price_surf, price_rect)
