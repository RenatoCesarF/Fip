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

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 650
RIGHT_MARGIN = 10
TOP_MARGIN = 10
LEFT_MARGIN = 15 


# - [ ] BUG: FileNotFoundError: No file './pics/2026-07-26/CF0012.JPG' found in working directory '/Users/renatocesar/code/fip'.
# - [ ] BUG:    ~~~~^^ File "/Users/renatocesar/code/fip/./main.py", line 149, in main path = f"{source_dir}/{correct_image_name(image_names[cur_img_index])}" ~~~~~~~~~~~^^^^^^^^^^^^^^^ IndexError: list index out of range

# - [ ] Possibilitar escolha da pasta raiz 
# - [ ] Possibilitar rescaling ou pelo menos um fullscreen
# - [ ] Impossibilitar de passar da ultima foto, e antepassar da primeira foto.
# - [ ] Escrever um README sobre o uso/instalação.
# - [ ] Refatorar o sistema de input pra uma função a parte:
#   - [ ] Criar uma classe global do estado do programa
# - [ ] Colocar um icone de favorito que é preenchido ou despreenchido 
# - [ ] Desfavoritar imagens (deletar da pasta de favoritos)
# - [ ] Items que foram marcado pra serem deletados aparecem com algum visual diferente (?)
# - [ ] em algum lugar (topo, base) mostrar uma lista das fotos, próximas e anteriores de forma 
#        que vamos nos movimentando nessa lista. Essa lista vai ter icones também (deletado/favoritado)
# - [ ] popup ou dicas, sobre teclas pra usar o programa (importante)
# - [ ] sons de favorito e deleção, além de outros sons satisfatórios.


state = State()
should_load_image = False
work_dir = "./pics"
source_dir = f"{work_dir}/{datetime.today().strftime('%Y-%m-%d')}"
import_dir = "/Volumes/POLEN/DCIM/100MEDIA"
to_delete = []

pygame.init()
pygame.key.set_repeat()
font = pygame.font.Font(pygame.font.get_default_font(), 20)

def main():
    global state

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    pygame.display.set_caption("FIP - FilterIng Pictures")

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
                        state.curr_image = pygame.transform.rotate(state.curr_image, 90)
                        state.cur_rotation += 90
                    else:
                        state.curr_image = pygame.transform.rotate(state.curr_image, -90)
                        state.cur_rotation -= 90

                if keys[pygame.K_RETURN]:
                    state.cur_img_index += 1

                    state.is_cur_image_loaded = False

                if keys[pygame.K_TAB]:
                    state.cur_img_index -= 1
                    state.is_cur_image_loaded = False

                if keys[pygame.K_f]:
                    image_name = correct_image_name(image_names[state.cur_img_index])
                    shutil.copy(f"{source_dir}/{image_name}", f"./fav/{image_name}.JPG")
                    state.cur_img_index += 1
                    state.is_cur_image_loaded = False

                if keys[pygame.K_x]:
                    to_delete.append(correct_image_name(image_names[state.cur_img_index]))

                    state.cur_img_index += 1
                    state.is_cur_image_loaded = False

                if keys[pygame.K_b]:
                    if configs.current_background == (0,0,0):
                        configs.change_background(configs.theme_background[0], configs.theme_background[1], configs.theme_background[2])
                    else:
                        configs.change_background(0,0,0)


            if keys[pygame.K_i]:
                state.cur_scale += 0.05
                state.curr_image = pygame.transform.scale_by(state.raw_image, (state.cur_scale,state.cur_scale))
                state.curr_image = pygame.transform.rotate(state.curr_image, state.cur_rotation)

            if keys[pygame.K_o]:
                if state.cur_scale >= 0.025:
                    state.cur_scale -= 0.025
                    state.curr_image = pygame.transform.scale_by(state.raw_image, (state.cur_scale,state.cur_scale))
                    state.curr_image = pygame.transform.rotate(state.curr_image, state.cur_rotation)

            if keys[pygame.K_j]:
                state.cur_y_padding += 10

            if keys[pygame.K_k]:
                state.cur_y_padding -= 10

            if keys[pygame.K_h]:
                state.cur_x_padding += 10

            if keys[pygame.K_l]:
                state.cur_x_padding -= 10


        screen.fill((configs.current_background))

        write(screen, f"Image: {state.cur_img_index}/{len(image_names)}", (LEFT_MARGIN, TOP_MARGIN), (5,5, 5))
        if not state.is_cur_image_loaded:
            path = f"{source_dir}/{correct_image_name(image_names[state.cur_img_index])}"
            state.curr_image = pygame.image.load(path).convert()
            state.raw_image = state.curr_image
            state.curr_image = pygame.transform.scale_by(state.curr_image, (state.cur_scale , state.cur_scale))
            state.curr_image = pygame.transform.rotate(state.curr_image, state.cur_rotation)

            state.is_cur_image_loaded = True

        half_width = state.curr_image.get_width()/2 + state.cur_x_padding
        half_height = state.curr_image.get_height()/2 + state.cur_y_padding

        screen.blit(state.curr_image, 
                    ((SCREEN_WIDTH/2) - half_width,
                     (SCREEN_HEIGHT/2) - half_height))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


def write(screen, text, pos, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, pos)

def correct_image_name(og):
    if og.startswith("._"):
        return og[2:]
    return og


if  __name__ == "__main__":
    main()
