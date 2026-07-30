
import shutil
import os
import pygame

from scenes.scene import Scene
from scenes.filter_scene import FilterScene
from scenes.import_scene import ImportScene

from state import State
from globals import LEFT_MARGIN, RIGHT_MARGIN, TOP_MARGIN

from enums.home_option import HomeOption 
from graphic import Graphic
from configs import configs

class HomeScene(Scene):
    args: list[any]

    def __init__(self):
        self.filter_rect = pygame.Rect(0, 0, 260, 180)
        self.import_rect = pygame.Rect(0, 0, 260, 180)

        self.title_font = pygame.font.Font(None, 56)
        self.option_font = pygame.font.Font(None, 36)

    def process(self, state: State, graphic: Graphic):
        gap = 40
        total_width = self.filter_rect.width + self.import_rect.width + gap
        start_x = (graphic.screen_width - total_width) // 2
        y = (graphic.screen_height - self.filter_rect.height) // 2

        self.filter_rect.topleft = (start_x, y)
        self.import_rect.topleft = (
            start_x + self.filter_rect.width + gap,
            y,
        )

        title = self.title_font.render("Choose an option", True, (240, 240, 240))
        title_rect = title.get_rect(
            center=(graphic.screen_width // 2, y - 80),
        )
        graphic.screen.blit(title, title_rect)

        self.draw_option(
            graphic.screen,
            self.filter_rect,
            "Filter",
            state.home_selected_option == HomeOption.FILTER,
        )

        self.draw_option(
            graphic.screen,
            self.import_rect,
            "Import",
            state.home_selected_option == HomeOption.IMPORT,
        )

    def draw_option( self, screen: pygame.Surface, rect: pygame.Rect, text: str, selected: bool):
        if selected:
            background = (255, 192, 203)  # Rosa principal
            border = (255, 225, 230)
            text_color = (45, 30, 35)
        else:
            background = (75, 55, 65)
            border = (125, 90, 105)
            text_color = (245, 235, 240)

        pygame.draw.rect(
            screen,
            background,
            rect,
            border_radius=12,
        )

        pygame.draw.rect(
            screen,
            border,
            rect,
            width=3,
            border_radius=12,
        )

        label = self.option_font.render(
            text,
            True,
            text_color,
        )

        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)

    def handle_input(self, event: pygame.event.Event, state: State):
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

    def open_selected_option(self, state: State):
        if state.home_selected_option == HomeOption.FILTER:
            state.switch_scene(FilterScene())
            return

        state.switch_scene(ImportScene())
