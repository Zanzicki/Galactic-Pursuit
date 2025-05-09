from abc import ABC, abstractmethod


class Strategy(ABC):

    @abstractmethod
    def choose_action(self):
        pass