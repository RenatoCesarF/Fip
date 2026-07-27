import os
from os import walk
import shutil
import random
import sys
from datetime import datetime

import pygame
from urllib.parse import urlparse, unquote

from configs import configs

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650
RIGHT_MARGIN = 10
TOP_MARGIN = 10
LEFT_MARGIN = 15 

import_dir = "/Volumes/POLEN/DCIM/100MEDIA"
TODAY_STR = datetime.today().strftime('%Y-%m-%d')
work_dir = "./pics"
to_delete = []


pygame.init()
pygame.key.set_repeat()
font = pygame.font.Font(pygame.font.get_default_font(), 20)

def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.display.set_caption("FIP - FilterIng Pictures")

    cur_img_index = 0
    cur_scale = 0.15
    cur_rotation = 0
    cur_x_padding = 0
    cur_y_padding = 0

    is_cur_image_loaded = False
    curr_image = None
    should_load_image = False
    source_dir = f"{work_dir}/{TODAY_STR}"

    # IMPORTING FILES
    if should_load_image:
        shutil.copytree(import_dir, source_dir)

    image_names = next(walk(source_dir), (None, None, []))[2] 
    image_names = sorted(image_names)
    
    running = True
    # clock.tick(60)

    while running:

        for event in pygame.event.get():
            key_mode = pygame.key.get_mods()
            is_shift_on = key_mode == 1

            keys = pygame.key.get_pressed()

            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.KEYDOWN:
                if keys[pygame.K_r]:
                    if is_shift_on:
                        curr_image = pygame.transform.rotate(curr_image, 90)
                        cur_rotation += 90
                    else:
                        curr_image = pygame.transform.rotate(curr_image, -90)
                        cur_rotation -= 90

                if keys[pygame.K_RETURN]:
                    cur_img_index += 1

                    is_cur_image_loaded = False

                if keys[pygame.K_TAB]:
                    cur_img_index -= 1

                    is_cur_image_loaded = False

                if keys[pygame.K_f]:
                    shutil.copy(f"{source_dir}/{image_names[cur_img_index][2:]}", f"./fav/{image_names[cur_img_index][2:]}.JPG")
                    cur_img_index += 1
                    is_cur_image_loaded = False

                if keys[pygame.K_x]:
                    to_delete.append(image_names[cur_img_index][2:])

                    cur_img_index += 1
                    is_cur_image_loaded = False

                if keys[pygame.K_b]:
                    if configs.current_background == (0,0,0):
                        configs.change_background(configs.theme_background[0], configs.theme_background[1], configs.theme_background[2])
                    else:
                        configs.change_background(0,0,0)


            if keys[pygame.K_i]:
                cur_scale += 0.05
                curr_image = pygame.transform.scale_by(raw_image, (cur_scale,cur_scale))
                curr_image = pygame.transform.rotate(curr_image, cur_rotation)

            if keys[pygame.K_o]:
                if cur_scale >= 0.025:
                    cur_scale -= 0.025
                    curr_image = pygame.transform.scale_by(raw_image, (cur_scale,cur_scale))
                    curr_image = pygame.transform.rotate(curr_image, cur_rotation)

            if keys[pygame.K_j]:
                cur_y_padding += 10

            if keys[pygame.K_k]:
                cur_y_padding -= 10

            if keys[pygame.K_h]:
                cur_x_padding += 10

            if keys[pygame.K_l]:
                cur_x_padding -= 10


        screen.fill((configs.current_background))

        write(screen, f"Image: {cur_img_index}/{len(image_names)}", (LEFT_MARGIN, TOP_MARGIN), (5,5, 5))
        if not is_cur_image_loaded:
            path = f"{source_dir}/{image_names[cur_img_index][2:]}"
            curr_image = pygame.image.load(path).convert()
            raw_image = curr_image
            curr_image = pygame.transform.scale_by(curr_image, (cur_scale , cur_scale))
            curr_image = pygame.transform.rotate(curr_image, cur_rotation)

            is_cur_image_loaded = True

        half_width = curr_image.get_width()/2 + cur_x_padding
        half_height = curr_image.get_height()/2 + cur_y_padding

        screen.blit(curr_image, 
                    ((SCREEN_WIDTH/2) - half_width,
                     (SCREEN_HEIGHT/2) - half_height))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


def write(screen, text, pos, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)


if  __name__ == "__main__":
    main()
