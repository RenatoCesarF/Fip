import os
import shutil
from os import walk
import random
import sys
from datetime import datetime

import pygame
from urllib.parse import urlparse, unquote

from configs import configs
from state import State
from utils import correct_image_name
from graphic import Graphic
from scenes.home_scene import HomeScene
from scenes.import_scene import ImportScene
from scenes.filter_scene import FilterScene
from globals import LEFT_MARGIN, RIGHT_MARGIN, TOP_MARGIN, INITIAL_HEIGHT, INITIAL_WIDTH 

# - [ ] Escrever um README sobre o uso/instalação.
# - [ ] Criar tela de importação, onde seleciona-se uma pasta, e clica em importar pra carregar os arquivos e ir pra página de filtros
# - [ ] popup ou dicas, sobre teclas pra usar o programa (importante) (criar um módulo pra isso, de legendas com téclas)
# - [ ] sons de favorito e deleção, além de outros sons satisfatórios pra rotacionar a aproximar.
# - [ ] Logo simples de um coelhinho escolhendo fotos, colocar na HOME e no topo do filtro.
# - [ ] Finalização: Decide se quer apagar todas as fotos colocadas como apagar da pasta original e apaga

# - [ ] BUG: Não da pra favoritar a última foto da coleção


def main():
    pygame.init()
    pygame.key.set_repeat()
    font = pygame.font.Font(pygame.font.get_default_font(), 20)

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((INITIAL_WIDTH, INITIAL_HEIGHT), pygame.RESIZABLE)

    pygame.display.set_caption("FIP - FilterIng Pictures")

    graphics = Graphic(screen, font)
    state = State(HomeScene())
    state.load_favorites()

    # IMPORTING FILES
    if state.should_load_image:
        shutil.copytree(import_dir, state.source_dir)

    state.load_working_directory()

    while state.running:
        graphics.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state.running = False
                break

            state.curr_scene.handle_input(event, state)

        screen.fill((30, 22, 27))

        state.curr_scene.process(state, graphics)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if  __name__ == "__main__":
    main()
