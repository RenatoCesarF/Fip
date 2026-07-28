import os
from os import walk
import shutil
import random
import sys
from datetime import datetime

import pygame
from urllib.parse import urlparse, unquote

from configs import configs
from state import State
from utils import correct_image_name

RIGHT_MARGIN = 10
TOP_MARGIN = 10
LEFT_MARGIN = 15 

# - [ ] Escrever um README sobre o uso/instalação.
# - [ ] Possibilitar escolha da pasta raiz  (CLI )
# - [ ] Escolher se carrega ou não as fotos
# - [ ] popup ou dicas, sobre teclas pra usar o programa (importante)
# - [ ] sons de favorito e deleção, além de outros sons satisfatórios.
# - [ ] Finalização: Decide se quer apagar todas as fotos colocadas como apagar da pasta original e apaga

# OVER
# - [ ] em algum lugar (topo, base) mostrar uma lista das fotos, próximas e anteriores de forma 
#        que vamos nos movimentando nessa lista. Essa lista vai ter icones também (deletado/favoritado)

state = State()
running = True
should_load_image = False

work_dir = "./pics"
source_dir = f"{work_dir}/2026-07-26"#{datetime.today().strftime('%Y-%m-%d')}"
import_dir = "/Volumes/POLEN/DCIM/100MEDIA"
to_delete = []

favs = []
favs = next(walk("./fav"), (None, None, []))[2] 
favs = sorted(favs)
favs = [correct_image_name(img) for img in favs]

pygame.init()
pygame.key.set_repeat()
font = pygame.font.Font(pygame.font.get_default_font(), 20)

def main():
    global running
    screen_width = 800
    screen_height = 650
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    pygame.display.set_caption("FIP - FilterIng Pictures")

    heart_icon = pygame.image.load("./assets/fav.png").convert_alpha()
    heart_icon = pygame.transform.scale_by(heart_icon, (0.05,0.05))

    trash_icon = pygame.image.load("./assets/trash.png").convert_alpha()
    trash_icon = pygame.transform.scale_by(trash_icon, (0.08,0.08))

    # IMPORTING FILES
    if should_load_image:
        shutil.copytree(import_dir, source_dir)

    image_names = next(walk(source_dir), (None, None, []))[2] 
    image_names = sorted(image_names)
    image_names = [correct_image_name(img) for img in image_names]

    while running:
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        handle_inputs(image_names)
        screen.fill((configs.current_background))

        write(screen, f"Image: {state.cur_img_index + 1}/{len(image_names)}", (LEFT_MARGIN, TOP_MARGIN), (5,5, 5))

        if not state.is_cur_image_loaded:
            load_image(image_names)

        state.draw_current_image(screen, screen_width, screen_height)

        # Heart Icon ----
        if image_names[state.cur_img_index] not in favs:
           fill(heart_icon, (50,50,50, 200))
        else:
           fill(heart_icon, (250,50,50, 255))

        screen.blit(heart_icon, (LEFT_MARGIN, screen_height - 70))

        # ----
        if image_names[state.cur_img_index]in to_delete:
            fill(trash_icon, (121,92,48, 255))
            screen.blit(trash_icon, (LEFT_MARGIN + 70, screen_height - 70))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

def write(screen, text, pos, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

def load_image(image_names):
    path = f"{source_dir}/{image_names[state.cur_img_index]}"
    state.load_image(path)

def handle_inputs(image_names):
    global running
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
                    state.rotate_image(90)
                else:
                    state.rotate_image(-90)

            if keys[pygame.K_RETURN]:
                if state.cur_img_index >= len(image_names) - 1:
                    return
                state.change_index(1)

            if keys[pygame.K_TAB]:
                if state.cur_img_index <= 0:
                    state.cur_img_index = len(image_names)
                state.change_index(-1)

            if keys[pygame.K_f]:
                if state.cur_img_index >= len(image_names) - 1:
                    return
                image_name = image_names[state.cur_img_index]
                if image_name in favs:
                    favs.remove(image_name)
                    os.remove(f"./fav/{image_name}.JPG")
                else:
                    shutil.copy(f"{source_dir}/{image_name}", f"./fav/{image_name}.JPG")
                    favs.append(image_name)

            if keys[pygame.K_x]:
                if state.cur_img_index >= len(image_names) - 1:
                    return

                image_name = image_names[state.cur_img_index]
                if image_name in to_delete:
                    to_delete.remove(image_names[state.cur_img_index])
                else:
                    to_delete.append(image_names[state.cur_img_index])

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


def is_image_favorite(favs, image):
    if image in favs:
        return True
    return False

def fill(surface, color):
    """Fill all pixels of the surface with color, preserve transparency."""
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))

if  __name__ == "__main__":
    main()
