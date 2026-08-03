import os
import pygame

from scenes.scene import Scene
from globals import LEFT_MARGIN, RIGHT_MARGIN, TOP_MARGIN

class DeleteScene(Scene):

    def __init__(self):
        self.passes = 0
        self.no_rect = pygame.Rect(0, 0, 230, 120)
        self.yes_rect = pygame.Rect(0, 0, 230, 120)
        self.options_rect = pygame.Rect(0, 0, 280, 70)
        pass

    def process(self, state, graphic):
        center_x = graphic.screen_width // 2
        title = graphic.font.render(
            "Would you like to delete the files marked as trash?",
            True,
            (245, 235, 240),
        )

        title_rect = title.get_rect(
            center=(center_x, graphic.screen_height // 2 - 180)
        )

        graphic.screen.blit(title, title_rect)

        gap = 40
        total_width = self.no_rect.width + self.yes_rect.width + gap
        start_x = (graphic.screen_width - total_width) // 2
        y = (graphic.screen_height - self.no_rect.height) // 2

        self.no_rect.topleft = (start_x, y)
        self.yes_rect.topleft = (
            start_x + self.no_rect.width + gap,
            y,
        )

        graphic.draw_button(
            self.no_rect,
            "No",
            not state.delete_selecteds,
        )

        graphic.draw_button(
            self.yes_rect,
            "Yes",
            state.delete_selecteds,
        )


    def handle_input(self, event: pygame.event.Event, state):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                state.delete_selecteds = not state.delete_selecteds

            elif event.key == pygame.K_RETURN:
                self.act_as_option(state)

        elif event.type == pygame.MOUSEMOTION:
            if self.no_rect.collidepoint(event.pos):
                state.delete_selecteds = False

            elif self.yes_rect.collidepoint(event.pos):
                state.delete_selecteds = True

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.no_rect.collidepoint(event.pos):
                state.delete_selecteds = False
                self.act_as_option(state)

            elif self.yes_rect.collidepoint(event.pos):
                state.delete_selecteds = True
                self.act_as_option(state)

    def act_as_option(self, state):
        if state.delete_selecteds == False:
            state.switch_scene('home')
            return

        state.delete_files_trashed()
        state.switch_scene('home')




