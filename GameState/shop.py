import pygame
import random
import pygame_gui
from Components import artifact, card
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
        all_cards = self.repository.fetch_all_card_names()
        all_artifacts = self.repository.fetch_all_artifact_names()
        cards = random.sample(all_cards, min(3, len(all_cards)))
        artifacts = random.sample(all_artifacts, min(2, len(all_artifacts)))
        self.gold_shop_items = {
            'cards': cards,
            'artifacts': artifacts
        }
        self.scrap_shop_items = {
            'upgrade': random.sample(upgrades.selected_dictionaries, 3),
            'repair': ['Repair Bot']
        }

    # -------------------- UI Creation --------------------
    def create_ui_elements(self):
        self.buttons.clear()
        # Cards
        for i, item in enumerate(self.gold_shop_items['cards']):
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((50 + i * 200, 100), (180, 60)),
                text=f"{item} ({self.item_gold_prices['card']}g)",
                manager=self.manager
            )
            self.buttons.append(('card', item, button))
        # Upgrades
        for i, item in enumerate(self.scrap_shop_items['upgrade']):
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((50 + i * 200, 200), (180, 60)),
                text=f"{item} ({self.item_scrap_prices['upgrade']}g)",
                manager=self.manager
            )
            self.buttons.append(('upgrade', item, button))
        # Artifacts
        for i, item in enumerate(self.gold_shop_items['artifacts']):
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((50 + i * 200, 300), (180, 60)),
                text=f"{item} ({self.item_gold_prices['artifact']}g)",
                manager=self.manager
            )
            self.buttons.append(('artifact', item, button))
        # Repairs
        for i, item in enumerate(self.scrap_shop_items['repair']):
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((50 + i * 200, 400), (320, 60)),
                text=f"{item} ({self.item_scrap_prices['repair']}g)",
                manager=self.manager
            )
            self.buttons.append(('repair', item, button))
        # Exit
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((490, 500), (100, 50)),
            text='Exit',
            manager=self.manager
        )

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
            for item_type, item_name, button in self.buttons:
                if event.ui_element == button:
                    if item_type == 'card':
                        self.buy_card(item_name)
                    elif item_type == 'artifact':
                        self.buy_artifact(item_name)
                    elif item_type == 'upgrade':
                        self.handle_upgrade()
                    elif item_type == 'repair':
                        self.handle_repair()
            if event.ui_element == self.exit_button:
                print("Returning to map!")
                self._game_world.state_changed_to_shop = "out"
        self.manager.process_events(event)

    # -------------------- Card Service --------------------
    def buy_card(self, card_name):
        item_cost = self.item_gold_prices['card']
        if self.player._credits >= item_cost:
            self.player.credits -= item_cost
            self.player_inventory.append(card_name)
            print(f"Bought {card_name} for {item_cost} gold.")
            # TODO: Add card to player's deck and database here
        else:
            print("Not enough gold.")

    # -------------------- Artifact Service --------------------
    def buy_artifact(self, artifact_name):
        item_cost = self.item_gold_prices['artifact']
        if self.player._credits >= item_cost:
            artifact_data = self.repository.fetch_artifact_by_name(artifact_name)
            if not artifact_data:
                print("Artifact not found!")
                return
            self.player.credits -= item_cost
            self.repository.insert_player_artifact(self.player._id, artifact_data[0])
            # Draw artifact in game using ArtifactFactory
            artifact_go = self.artifact_factory.create_component(artifact_data)
            self.player.artifacts.append(artifact_go)
            self._game_world.instantiate(artifact_go)
            self.player.update_artifacts()
            print(f"Bought {artifact_name} for {item_cost} gold.")
        else:
            print("Not enough gold.")

    # -------------------- Upgrade Service --------------------
    def handle_upgrade(self):
        if self.player._scraps >= self.item_scrap_prices['upgrade']:
            self.show_upgrade_card_window()
        else:
            print("Not enough scrap for upgrade.")

    def show_upgrade_card_window(self):
        player_deck = self.self._game_world.player.deck
        card_names = [card.name for card in player_deck.decklist]
        print("Select a card to upgrade:")
        for index, card_name in enumerate(card_names):
            print(f"{index + 1}: {card_name}")
        if card_names:
            self.upgrade_card(card_names[0])

    def upgrade_card(self, card_name):
        player_deck = self.self._game_world.player.deck
        card_to_upgrade = next((card for card in player_deck.decklist if card.name == card_name), None)
        if card_to_upgrade:
            card_to_upgrade.upgraded = True
            self.player._scraps -= self.item_scrap_prices['upgrade']
            print(f"Upgraded {card_to_upgrade.name}!")
            # TODO: Optionally update the database here
        else:
            print("Card not found in deck.")

    # -------------------- Repair Service --------------------
    def handle_repair(self):
        if self.player._scraps >= self.item_scrap_prices['repair']:
            self.heal_player()
            self.player.scraps -= self.item_scrap_prices['repair']
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
        self.ui_element.draw("Intergalactic Trade Sector", (640, 40), self.player._credits, self.player._scraps, self.player._health, self.player._max_health)
