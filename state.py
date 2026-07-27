import pygame

class State:
    cur_img_index: int

    cur_rotation: int
    cur_x_padding: int
    cur_y_padding: int
    cur_scale: float

    is_cur_image_loaded: bool
    curr_image: object
    raw_image: object

    def __init__(self):
        self.cur_img_index = 0

        self.cur_rotation = 0
        self.cur_x_padding = 0
        self.cur_y_padding = 0
        self.cur_scale = 0.15

        self.is_cur_image_loaded = False
        self.curr_image = None
        self.raw_image = None

    def rotate_image(self, amount: int):
        self.curr_image = pygame.transform.rotate(self.curr_image, amount)
        self.cur_rotation += amount

    def change_index(self, amount):
        self.cur_img_index += amount
        self.is_cur_image_loaded = False

    def zoom_image(self, amount):
        if self.cur_scale <= 0.025:
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
