
import shutil
import os
import pygame

from scenes.scene import Scene

from globals import LEFT_MARGIN, RIGHT_MARGIN, TOP_MARGIN

from enums.home_option import HomeOption 
from graphic import Graphic
from colors import Colors
from logo import Logo
from configs import configs

class HomeScene(Scene):
    args: list[any]

    def __init__(self):
        self.filter_rect = pygame.Rect(0, 100, 240, 150)
        self.import_rect = pygame.Rect(0, 100, 240, 150)

        self.title_font = pygame.font.Font(None, 56)
        self.option_font = pygame.font.Font(None, 36)

    def process(self, state, graphic: Graphic):
        gap = 40
        total_width = self.filter_rect.width + self.import_rect.width + gap
        start_x = (graphic.screen_width - total_width) // 2
        y = (graphic.screen_height - self.filter_rect.height + 100) // 2

        self.filter_rect.topleft = (start_x, y + 30)
        self.import_rect.topleft = (
            start_x + self.filter_rect.width + gap,
            y + 30,
        )

        w,h = Logo.large.get_size()
        graphic.screen.blit(Logo.large,  (graphic.screen_width // 2 - w/2, y - 280))

        title = self.title_font.render("Choose an option", True, Colors.white)
        title_rect = title.get_rect(
            center=(graphic.screen_width // 2, y + 250),
        )
        graphic.screen.blit(title, title_rect)

        graphic.draw_button(
            self.filter_rect,
            "Filter",
            state.home_selected_option == HomeOption.FILTER,
        )

        graphic.draw_button(
            self.import_rect,
            "Import",
            state.home_selected_option == HomeOption.IMPORT,
        )

    def handle_input(self, event: pygame.event.Event, state):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                state.change_selected_button_home()

            elif event.key == pygame.K_RETURN:
                self.open_selected_option(state)

        elif event.type == pygame.MOUSEMOTION:
            if self.filter_rect.collidepoint(event.pos):
                state.home_selected_option = HomeOption.FILTER

            elif self.import_rect.collidepoint(event.pos):
                state.home_selected_option = HomeOption.IMPORT

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.filter_rect.collidepoint(event.pos):
                state.home_selected_option = HomeOption.FILTER
                self.open_selected_option(state)

            elif self.import_rect.collidepoint(event.pos):
                state.home_selected_option = HomeOption.IMPORT
                self.open_selected_option(state)

    def open_selected_option(self, state):
        if state.home_selected_option == HomeOption.FILTER:
            state.switch_scene("filter")
            return

        state.switch_scene("import")
