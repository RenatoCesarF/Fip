import pygame
from globals import INITIAL_HEIGHT, INITIAL_WIDTH 

class Graphic:
    screen: pygame.Surface
    font: pygame.font
    screen_height: int
    screen_width: int

    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.screen_width = INITIAL_WIDTH
        self.screen_height = INITIAL_HEIGHT

    def update(self):
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()

    def write(self, text, pos, color):
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, pos)

    def fill(self, surface, color):
        """Fill all pixels of the surface with color, preserve transparency."""
        w, h = surface.get_size()
        r, g, b, _ = color
        for x in range(w):
            for y in range(h):
                a = surface.get_at((x, y))[3]
                surface.set_at((x, y), pygame.Color(r, g, b, a))

