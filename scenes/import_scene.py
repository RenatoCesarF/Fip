import os
import tkinter as tk


from file_picker_py import pick_folder_blocking
import pygame

from scenes.scene import Scene
from graphic import Graphic

class ImportScene(Scene):
    def __init__(self):
        self.selected_folder: str | None = None
        self.file_count = 0

        self.selected_button = 0

        self.choose_folder_rect = pygame.Rect(0, 0, 280, 70)
        self.import_rect = pygame.Rect(0, 0, 280, 70)


    def process(self, state, graphic: Graphic):
        center_x = graphic.screen_width // 2

        if state.is_loading:
            title = graphic.font.render(
                "Carregando",
                True,
                (245, 235, 240),
            )

            title_rect = title.get_rect(
                center=(center_x, graphic.screen_height // 2 - 180)
            )
            graphic.screen.blit(title, title_rect)
            return


        title = graphic.font.render(
            "Importar arquivos",
            True,
            (245, 235, 240),
        )

        title_rect = title.get_rect(
            center=(center_x, graphic.screen_height // 2 - 180)
        )


        graphic.screen.blit(title, title_rect)

        self.choose_folder_rect.center = (
            center_x,
            graphic.screen_height // 2 - 70,
        )

        graphic.draw_button(
            self.choose_folder_rect,
            "Escolher pasta",
            self.selected_button == 0,
        )

        if self.selected_folder:
            count_text = graphic.font.render(
                f"{self.file_count} arquivo(s) encontrado(s)",
                True,
                (245, 235, 240),
            )

            count_rect = count_text.get_rect(
                center=(center_x, graphic.screen_height // 2 + 10)
            )

            graphic.screen.blit(count_text, count_rect)

            folder_name = os.path.basename(self.selected_folder)

            folder_text = graphic.font.render(
                folder_name,
                True,
                (190, 165, 175),
            )

            folder_rect = folder_text.get_rect(
                center=(center_x, graphic.screen_height // 2 + 42)
            )

            graphic.screen.blit(folder_text, folder_rect)

            self.import_rect.center = (
                center_x,
                graphic.screen_height // 2 + 115,
            )

            graphic.draw_button(
                self.import_rect,
                "Importar",
                self.selected_button == 1,
            )


    def handle_input(self, event, state):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                if self.selected_folder:
                    self.selected_button = (
                        self.selected_button + 1
                    ) % 2

            elif event.key in (
                pygame.K_RETURN,
                pygame.K_SPACE,
            ):
                self.execute_selected_action(state)

        elif event.type == pygame.MOUSEMOTION:
            if self.choose_folder_rect.collidepoint(event.pos):
                self.selected_button = 0

            elif (
                self.selected_folder
                and self.import_rect.collidepoint(event.pos)
            ):
                self.selected_button = 1

        elif (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            if self.choose_folder_rect.collidepoint(event.pos):
                self.select_folder()

            elif (
                self.selected_folder
                and self.import_rect.collidepoint(event.pos)
            ):
                self.import_and_switch(state)

    def import_and_switch(self, state):
        state.import_files(self.selected_folder)
        state.load_working_directory()
        state.switch_scene('filter')

    def execute_selected_action(self, state):
        if self.selected_button == 0:
            self.select_folder()
            return

        if self.selected_folder:
            self.import_and_switch(state)

    def select_folder(self):
        folder = pick_folder_blocking()

        if not folder:
            return

        self.selected_folder = folder

        self.file_count = sum(
            1
            for item in os.scandir(folder)
            if item.is_file()
        )

        self.selected_button = 1

        # Remove eventos de teclado acumulados enquanto
        # o seletor de pasta estava aberto.
        pygame.event.clear()

