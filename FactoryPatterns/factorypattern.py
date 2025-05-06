from abc import ABC, abstractmethod

class Factory(ABC): 
    @abstractmethod 
    def create_component(self): 
        pass

