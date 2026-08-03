import shutil
import os
import pygame

import os, glob

from scenes.scene import Scene
from globals import LEFT_MARGIN, RIGHT_MARGIN, TOP_MARGIN
from sounds import Sounds
from logo import Logo

class FilterScene(Scene):
    heart_icon: pygame.Surface
    trash_icon: pygame.Surface

    def __init__(self, state):
        self.heart_icon = pygame.image.load("./assets/fav.png").convert_alpha()
        self.heart_icon = pygame.transform.scale_by(self.heart_icon, (0.05,0.05))

        self.trash_icon = pygame.image.load("./assets/trash.png").convert_alpha()
        self.trash_icon = pygame.transform.scale_by(self.trash_icon, (0.08,0.08))

        state.cur_img_index = 0
        state.is_cur_image_loaded = False
        state.imported_images = []
 
    def process(self, state, graphics):
        if(len(state.imported_images) == 0):
            last_dir = max([os.path.join('./pics',d) for d in os.listdir("./pics")], key=os.path.getmtime)
            state.source_dir = last_dir
            state.load_working_directory()
            return

        if not state.focus:
            small_logo = pygame.transform.scale_by(Logo.square, (0.2, 0.2))
            graphics.screen.blit(small_logo, (LEFT_MARGIN, TOP_MARGIN))

            amount_x = graphics.screen_width - RIGHT_MARGIN - 120
            graphics.write(f"Image: {state.cur_img_index + 1}/{len(state.imported_images)}", (amount_x, TOP_MARGIN), (205,205, 205))

        if not state.is_cur_image_loaded:
            self.load_image(state)

        state.draw_current_image(graphics.screen, graphics.screen_width, graphics.screen_height)

        # Heart Icon ----
        if state.focus:
            return
        if state.imported_images[state.cur_img_index] not in state.favs:
           graphics.fill(self.heart_icon, (50,50,50, 200))
        else:
           graphics.fill(self.heart_icon, (250,50,50, 255))

        graphics.screen.blit(self.heart_icon, (LEFT_MARGIN, graphics.screen_height - 70))

        # Trash Icon ----
        if state.imported_images[state.cur_img_index]in state.to_delete:
            graphics.fill(self.trash_icon, (121,92,48, 255))
            graphics.screen.blit(self.trash_icon, (LEFT_MARGIN + 70, graphics.screen_height - 70))

    def load_image(self, state):
        path = f"{state.source_dir}/{state.imported_images[state.cur_img_index]}"
        state.load_image(path)

    def handle_input(self, event, state):
        key_mode = pygame.key.get_mods()
        is_shift_on = key_mode == 1

        keys = pygame.key.get_pressed()

        if event.type == pygame.KEYDOWN:
            if keys[pygame.K_r]:
                Sounds.rotate.play()
                if is_shift_on:
                    state.rotate_image(90)
                else:
                    state.rotate_image(-90)

            if keys[pygame.K_RETURN]:
                if state.cur_img_index == len(state.imported_images) -1:
                    state.switch_scene('delete')
                    return

                Sounds.passing.play()
                state.change_index(1)

            if keys[pygame.K_TAB]:
                if state.cur_img_index <= 0:
                    state.cur_img_index = len(state.imported_images)

                Sounds.passing.play()
                state.change_index(-1)

            if keys[pygame.K_f]:
                if state.cur_img_index >= len(state.imported_images):
                    return

                Sounds.favorite.play()
                image_name = state.imported_images[state.cur_img_index]
                if image_name in state.favs:
                    state.favs.remove(image_name)
                    os.remove(f"./fav/{image_name}")
                else:
                    shutil.copy(f"{state.source_dir}/{image_name}", f"./fav/{image_name}")
                    state.favs.append(image_name)

            if keys[pygame.K_x]:
                if state.cur_img_index >= len(state.imported_images):
                    return

                Sounds.trash.play()
                image_name = state.imported_images[state.cur_img_index]
                if image_name in state.to_delete:
                    state.to_delete.remove(state.imported_images[state.cur_img_index])
                else:
                    state.to_delete.append(state.imported_images[state.cur_img_index])

            if keys[pygame.K_b]:
                state.focus = not state.focus

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


