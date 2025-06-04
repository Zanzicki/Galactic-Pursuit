from abc import ABC, abstractmethod

from gameobject import GameObject

class Builder(ABC):
    
    @abstractmethod
    def build(self):
        pass

    @abstractmethod
    def get_gameObject(self) -> GameObject:
        pass