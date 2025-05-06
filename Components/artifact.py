from Components.component import Component

class Artifact(Component):
    def __init__(self, name, rarity):
        super().__init__()
        self._name = name
        self._rarity = rarity

    @property
    def name(self):
        return self._name
    
    @property
    def rarity(self):
        return self._rarity

    def awake(self, game_world):
        pass

    def start(self):
        pass

    def update(self, delta_time):
        pass