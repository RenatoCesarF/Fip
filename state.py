from os import walk
import shutil

import pygame

from enums.home_option import HomeOption 
from utils import correct_image_name
from scenes.scene import SceneEnum, Scene

class State:
    curr_scene: Scene
    running: bool

    source_dir: str
    import_dir: str

    cur_img_index: int

    cur_rotation: int
    cur_x_padding: int
    cur_y_padding: int
    cur_scale: float

    favs: list[str]
    to_delete: list[str]
    imported_images: list[str]

    is_cur_image_loaded: bool
    curr_image: object
    raw_image: object

    home_selected_option: HomeOption

    def __init__(self, scene):
        self.curr_scene = scene

        self.running = True

        self.source_dir = f"./pics"#{datetime.today().strftime('%Y-%m-%d')}"
        self.import_dir = "/Volumes/POLEN/DCIM/100MEDIA"

        self.favs = []
        self.to_delete = []
        self.imported_images = []

        self.cur_img_index = 0

        self.cur_rotation = 0
        self.cur_x_padding = 0
        self.cur_y_padding = 0
        self.cur_scale = 0.15

        self.is_cur_image_loaded = False
        self.curr_image = None
        self.raw_image = None

        #---- HOME ----
        self.home_selected_option = HomeOption.FILTER

    def switch_scene(self, scene: Scene):
        self.curr_scene = scene

    def load_favorites(self):
        self.favs = sorted(next(walk("./fav"), (None, None, []))[2])
        self.favs = [correct_image_name(img) for img in self.favs]
    
    def load_working_directory(self):
        self.imported_images = sorted(next(walk(self.source_dir), (None, None, []))[2])
        self.imported_images = [correct_image_name(img) for img in self.imported_images]

    def import_files(self, import_dir):
        shutil.copytree(import_dir, state.source_dir)

    def rotate_image(self, amount: int):
        self.curr_image = pygame.transform.rotate(self.curr_image, amount)
        self.cur_rotation += amount

    def change_index(self, amount):
        self.cur_img_index += amount
        self.is_cur_image_loaded = False

    def zoom_image(self, amount):
        if self.cur_scale <= 0.025 and amount < 0:
            return
        self.cur_scale += amount
        self.curr_image = pygame.transform.scale_by(self.raw_image, (self.cur_scale, self.cur_scale))
        self.curr_image = pygame.transform.rotate(self.curr_image, self.cur_rotation)

    def draw_current_image(self, screen, width, height):
        half_width = self.curr_image.get_width()/2 + self.cur_x_padding
        half_height = self.curr_image.get_height()/2 + self.cur_y_padding

        screen.blit(self.curr_image, 
                    ((width/2) - half_width,
                     (height/2) - half_height))

    def load_image(self, path):
        self.curr_image = pygame.image.load(path).convert()
        self.raw_image = self.curr_image
        self.curr_image = pygame.transform.scale_by(self.curr_image, (self.cur_scale , self.cur_scale))
        self.curr_image = pygame.transform.rotate(self.curr_image, self.cur_rotation)

        self.is_cur_image_loaded = True

    def change_selected_button_home(self):
        if self.home_selected_option == HomeOption.FILTER:
            self.home_selected_option = HomeOption.IMPORT
            return

        self.home_selected_option = HomeOption.FILTER
