import pygame
from enum import Enum

from abc import ABC, abstractmethod

class SceneEnum(Enum):
    MENU = 0
    CHOSE_FOLDER = 1
    FILTER = 2
    FINISH = 3

class Scene(ABC):
    @abstractmethod
    def process(self):
        """Every payment method must implement this."""
        pass

    @abstractmethod
    def handle_input(self, event, state):
        pass


