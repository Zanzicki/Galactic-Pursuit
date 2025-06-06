import pygame
import pygame_gui
import random

from Components.player import Player
from Database.sqlrepository import SQLRepository
from FactoryPatterns.artifactFactory import ArtifactFactory
from FactoryPatterns.cardfactory import CardFactory
from UI.currency import Currency
from Components.card import Card

class MysteryPlanetState:
    def __init__(self, game_world):
        self.game_world = game_world
        self.artifact_factory = ArtifactFactory()
        self.card_factory = CardFactory()
        self.player = Player.get_instance()
        self.repository = SQLRepository()
        self.manager = game_world.ui_manager.ui_manager
        self.screen = game_world.screen
        self.reward = None
        self.reward_type = None
        self.claim_button = None
        self.font = pygame.font.Font(None, 36)
        self.currency = Currency()
        self.reward_id = None

    def enter(self):
        # Randomly choose a reward type
        self.reward_type = random.choice(["artifact", "gold", "scraps", "heal", "card"])
        if self.reward_type == "artifact":
            artifact_data = self.repository.fetch_random_artifact()
            self.reward_id = artifact_data[0]
            self.reward = self.artifact_factory.create_component(artifact_data)
        elif self.reward_type == "gold":
            self.reward = random.randint(20, 100)
        elif self.reward_type == "scraps":
            self.reward = random.randint(10, 50)
        elif self.reward_type == "heal":
            self.reward = random.randint(10, 40)
        elif self.reward_type == "card":
            card_data = self.repository.fetch_random_card()
            self.reward_id = card_data[0]
            self.reward = self.card_factory.create_component(card_data)
        # Show claim button
        self.claim_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen.get_width()//2 - 75, self.screen.get_height()//2 + 100), (150, 50)),
            text="Claim Reward",
            manager=self.manager
        )

    def update(self, delta_time, events):
        for event in events:
            self.manager.process_events(event)
        self.manager.update(delta_time)

        for event in events:
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.claim_button:
                # Give reward and update database
                if self.reward_type == "artifact":
                    self.player.artifacts.append(self.reward)
                    self.repository.insert_player_artifact(self.player._id, self.reward_id)
                elif self.reward_type == "gold":
                    self.currency.addCredit(self.reward)
                elif self.reward_type == "scraps":
                    self.currency.addScrap(self.reward)
                elif self.reward_type == "heal":
                    self.player.health += self.reward
                    self.repository.update_player_currency(player_id=self.player._id, health=self.player._health)
                elif self.reward_type == "card":
                    card_display = self.reward.get_component("CardDisplay")
                    card_data = card_display.card_data
                    if isinstance(card_data, tuple):
                        card_data = Card(*card_data[1:7])
                    self.player.deck.add_card(card_data)
                    self.repository.insert_player_card(self.player._id, self.reward_id)
                self.claim_button.kill()
                self.game_world.GameState = "map"

    def draw(self):
        self.screen.fill((30, 30, 60))
        # Draw reward info
        if self.reward_type == "artifact":
            name = self.reward.get_component("Artifact")._name
            text = self.font.render(f"Artifact: {name}", True, (255, 255, 255))
        elif self.reward_type == "gold":
            text = self.font.render(f"Gold: +{self.reward}", True, (255, 215, 0))
        elif self.reward_type == "scraps":
            text = self.font.render(f"Scraps: +{self.reward}", True, (100, 200, 255))
        elif self.reward_type == "heal":
            text = self.font.render(f"Heal: +{self.reward}", True, (0, 255, 0))
        elif self.reward_type == "card":
            card_display = self.reward.get_component("CardDisplay")
            card_data = card_display.card_data
            # If card_data is a tuple, convert to Card object
            if isinstance(card_data, tuple):
                card_name = card_data[1]
            else:
                card_name = getattr(card_data, "_name", str(card_data))
            text = self.font.render(f"Card: {card_name}", True, (255, 255, 255))
        else:
            text = self.font.render("Mystery Reward!", True, (255, 255, 255))
        self.screen.blit(
            text,
            (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 - 50),
        )
        self.manager.draw_ui(self.screen)