import pygame
from Components.component import SpriteRenderer
from FactoryPatterns.factorypattern import Factory
from Components.artifact import Artifact
from gameobject import GameObject
from database import Database

class ArtifactFactory(Factory):
    def __init__(self):
        self.db = Database() 

    def create_component(self):
        artifacts = self.db.fetch_artifacts() 
        if not artifacts:
            raise ValueError("No artifacts found in the database.")

        artifact_data = artifacts[0]
        name, rarity, prize = artifact_data[1], artifact_data[2], artifact_data[3]

        go = GameObject(pygame.math.Vector2(50, 50))
        go.add_component(Artifact(name, rarity, prize))
        go.add_component(SpriteRenderer("Artifacts/Icon34.png")) 
        return go