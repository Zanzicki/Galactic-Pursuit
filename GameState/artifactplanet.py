import pygame
import pygame_gui

from Components.player import Player
from Database.sqlrepository import SQLRepository
from FactoryPatterns.artifactFactory import ArtifactFactory

class ArtifactPlanetState:
    def __init__(self, game_world):
        self.game_world = game_world
        self.artifact_factory = ArtifactFactory()
        self.player = Player.get_instance()
        self.repository = SQLRepository()
        self.manager = game_world.ui_manager.ui_manager
        self.screen = game_world.screen
        self.artifact = None
        self.artifact_id = None
        self.artifact_data = None
        self.claim_button = None
        self.font = pygame.font.Font(None, 36)

    def enter(self):
        # Generate or select an artifact
        self.artifact_data = self.repository.fetch_random_artifact()
        artifactgo = self.artifact_factory.create_component(self.artifact_data)
        self.artifact = artifactgo.get_component("Artifact")
        self.artifact_id = self.artifact_data[0] 
        # Show claim button
        self.claim_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen.get_width()//2 - 75, self.screen.get_height()//2 + 100), (150, 50)),
            text="Claim Artifact",
            manager=self.manager
        )

    def update(self, delta_time, events):
        for event in events:
            self.manager.process_events(event)
        self.manager.update(delta_time)

        for event in events:
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.claim_button:
                # Add artifact to player and database
                self.repository.insert_player_artifact(self.player._id, self.artifact_id)
                artifactgo = self.artifact_factory.create_component(self.artifact_data)
                self.game_world.instantiate(artifactgo)
                self.player.artifacts.append(artifactgo)
                self.player.update_artifacts()
                self.claim_button.kill()
                self.game_world.GameState = "map"  # Return to map

    def draw(self):
        self.screen.fill((30, 30, 60))
        # Draw artifact info
        if self.artifact:
            text = self.font.render(f"Artifact: {self.artifact._name}", True, (255, 255, 255))
            self.screen.blit(text, (self.screen.get_width()//2 - text.get_width()//2, self.screen.get_height()//2 - 50))
        self.manager.draw_ui(self.screen)