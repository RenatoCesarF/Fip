
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
