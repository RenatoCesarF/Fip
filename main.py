import os
from pathlib import Path
import sys

import pygame

from configs import configs
from state import State
from utils import correct_image_name
from colors import Colors
from graphic import Graphic
from scenes.home_scene import HomeScene
from scenes.import_scene import ImportScene
from scenes.filter_scene import FilterScene
from sounds import Sounds
from logo import Logo
from globals import LEFT_MARGIN, RIGHT_MARGIN, TOP_MARGIN, INITIAL_HEIGHT, INITIAL_WIDTH 

# - [ ] Escrever um README sobre o uso/instalação.
# - [ ] criar um módulo de legendas com téclas e o que elas fazem, cada tela vai ter o seu
# - [ ] Logo simples de um coelhinho escolhendo fotos, colocar na HOME e no topo do filtro.
# - [ ] Finalização: Decide se quer apagar todas as fotos colocadas como apagar da pasta original e apaga
# - [ ] Remover dependencia do Theme, pois nào faz mais sentido
# - [ ] Mute and unmute button

def main():
    pygame.init()
    pygame.key.set_repeat()

    font = pygame.font.Font(pygame.font.get_default_font(), 20)

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((INITIAL_WIDTH, INITIAL_HEIGHT), pygame.RESIZABLE)

    pygame.display.set_caption("FIP - FilterIng Pictures")

    icon = pygame.image.load("./assets/icon.png").convert_alpha()
    pygame.display.set_icon(icon)


    graphics = Graphic(screen, font)
    sounds = Sounds.load()
    logo = Logo.load()
    state = State(HomeScene())

    Path("./fav").mkdir(parents=True, exist_ok=True)
    Path("./pics").mkdir(parents=True, exist_ok=True)

    state.load_favorites()
    state.load_working_directory()

    while state.running:
        graphics.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state.running = False
                break

            state.curr_scene.handle_input(event, state)

        if state.focus:
            screen.fill((0,0,0))
        else:
            screen.fill(Colors.dark)

        state.curr_scene.process(state, graphics)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if  __name__ == "__main__":
    main()
