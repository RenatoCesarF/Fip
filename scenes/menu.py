
import shutil
import os
import pygame

from scenes.scene import Scene
from state import State
from globals import LEFT_MARGIN, RIGHT_MARGIN, TOP_MARGIN
from configs import configs
from utils import fill

class MenuScene(Scene):

    def __init__(self):
        pass

    def process(self, screen, state,  screen_width, screen_height):
        screen.fill((configs.current_background))

    def load_image(self, state):
        path = f"{state.source_dir}/{state.imported_images[state.cur_img_index]}"
        state.load_image(path)

    def handle_input(self, event, state: State):
        key_mode = pygame.key.get_mods()
        is_shift_on = key_mode == 1

        keys = pygame.key.get_pressed()

        if event.type == pygame.KEYDOWN:
            if keys[pygame.K_r]:
                if is_shift_on:
                    state.rotate_image(90)
                else:
                    state.rotate_image(-90)

            if keys[pygame.K_RETURN]:
                if state.cur_img_index >= len(state.imported_images) - 1:
                    return
                state.change_index(1)

            if keys[pygame.K_TAB]:
                if state.cur_img_index <= 0:
                    state.cur_img_index = len(state.imported_images)
                state.change_index(-1)

            if keys[pygame.K_f]:
                if state.cur_img_index >= len(state.imported_images) - 1:
                    return
                image_name = state.imported_images[state.cur_img_index]
                if image_name in state.favs:
                    state.favs.remove(image_name)
                    os.remove(f"./fav/{image_name}")
                else:
                    shutil.copy(f"{state.source_dir}/{image_name}", f"./fav/{image_name}")
                    state.favs.append(image_name)

            if keys[pygame.K_x]:
                if state.cur_img_index >= len(state.imported_images) - 1:
                    return

                image_name = state.imported_images[state.cur_img_index]
                if image_name in state.to_delete:
                    state.to_delete.remove(state.imported_images[state.cur_img_index])
                else:
                    state.to_delete.append(state.imported_images[state.cur_img_index])

            if keys[pygame.K_b]:
                if configs.current_background == (0,0,0):
                    configs.change_background(configs.theme_background[0], configs.theme_background[1], configs.theme_background[2])
                else:
                    configs.change_background(0,0,0)

        if keys[pygame.K_i]:
            state.zoom_image(0.05)

        if keys[pygame.K_o]:
            state.zoom_image(-0.025)

        if keys[pygame.K_j]:
            state.cur_y_padding -= 10

        if keys[pygame.K_k]:
            state.cur_y_padding += 10

        if keys[pygame.K_h]:
            state.cur_x_padding += 10

        if keys[pygame.K_l]:
            state.cur_x_padding -= 10


