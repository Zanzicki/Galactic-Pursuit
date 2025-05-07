from Components.component import Component

class Card(Component):
    def __init__(self, name, value, type, rarity, description, prize):
        super().__init__()
        self._name = name
        self._value = value
        self._type = type
        self._rarity = rarity
        self._description = description
        self._prize = prize

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value
    
    @property
    def type(self):
        return self._type

    def awake(self, game_world):
        pass

    def start(self):
        pass

    def update(self, delta_time):
        pass