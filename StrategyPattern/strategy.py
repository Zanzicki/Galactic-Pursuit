from abc import ABC, abstractmethod


class Strategy(ABC):
   
    @abstractmethod
    def choose_action(self):
        pass

    @abstractmethod
    def basic_attack(self):        
        pass

    @abstractmethod
    def basic_defense(self):        
        pass