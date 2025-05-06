from FactoryPatterns.factorypattern import Factory
from Components.artifact import Artifact

class ArtifactFactory(Factory):
    def create_component(self, name, value, type, rarity, description, image_path):
        return Artifact(name, value, type, rarity, description, image_path)