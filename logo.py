import pygame
class Logo:
    large: pygame.Surface
    square: pygame.Surface

    @classmethod
    def load(cls):
        cls.large = pygame.image.load("./assets/logo-large.png").convert_alpha()
        cls.square = pygame.image.load("./assets/logo-square.png").convert_alpha()
