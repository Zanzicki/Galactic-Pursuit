from abc import ABC, abstractmethod

class State(ABC):
    @abstractmethod
    def enter(self, boss, player):
        pass

    @abstractmethod
    def execute(self, boss, player):
        pass

    @abstractmethod
    def exit(self, boss, player):
        pass
