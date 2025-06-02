import pygame
from Components.component import SpriteRenderer
from FactoryPatterns.factorypattern import Factory
from Components.artifact import Artifact
from gameobject import GameObject
from Database.database import Database
import random

class ArtifactFactory(Factory):
    def __init__(self):
        self.db = Database() 

    def create_component(self):
        artifacts = self.db.fetch_artifacts() 
        if not artifacts:
            raise ValueError("No artifacts found in the database.")
        
        random_artifact = random.randint(0, len(artifacts) - 1)
        
        artifact_data = random_artifact[0]
        name, rarity, description, price = artifact_data[1], artifact_data[2], artifact_data[3], artifact_data[4]

        go = GameObject(pygame.math.Vector2(50, 50))
        go.add_component(Artifact(name, rarity, description, price))
        go.add_component(SpriteRenderer(f"Artifacts/{name}.png")) 
        return go

    def create_component(self, artifact_data):
        name, rarity, description, price = artifact_data[1], artifact_data[2], artifact_data[3], artifact_data[4]
        go = GameObject(pygame.math.Vector2(50, 50))
        go.add_component(Artifact(name, rarity, description, price))
        go.add_component(SpriteRenderer(f"Artifacts/{name}.png"))
        print(f"Artifact {name} created with rarity {rarity} and price {price}")
        return go