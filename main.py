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
from scenes.chose_folder import ChoseFolderScene
from scenes.filter import FilterScene
from globals import LEFT_MARGIN, RIGHT_MARGIN, TOP_MARGIN

# - [ ] Escrever um modulo de graphics que contem screen, fill e write com utils (screen_width e height tmb)
# - [ ] Escrever um README sobre o uso/instalação.
# - [ ] Possibilitar escolha da pasta raiz  (CLI )
# - [ ] Escolher se carrega ou não as fotos
# - [ ] popup ou dicas, sobre teclas pra usar o programa (importante)
# - [ ] sons de favorito e deleção, além de outros sons satisfatórios.
# - [ ] Finalização: Decide se quer apagar todas as fotos colocadas como apagar da pasta original e apaga

work_dir = ""
import_dir = "/Volumes/POLEN/DCIM/100MEDIA"

state = State()
state.load_favorites()

pygame.init()
pygame.key.set_repeat()
font = pygame.font.Font(pygame.font.get_default_font(), 20)

def main():
    screen_width = 800
    screen_height = 650

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    pygame.display.set_caption("FIP - FilterIng Pictures")

    # IMPORTING FILES
    if state.should_load_image:
        shutil.copytree(import_dir, state.source_dir)

    state.load_working_directory()

    scene = FilterScene()

    while state.running:
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state.running = False
                break

            scene.handle_input(event, state)

        scene.process(screen, state, screen_width, screen_height)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if  __name__ == "__main__":
    main()
