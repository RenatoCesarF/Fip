class Configs:
    current_background: str
    theme_background: str

    def __init__(self):
        self.current_background = 30, 22, 27
        self.theme_background = 30, 22, 27

    def change_background(self,r,g,b):
        self.current_background = (r,g,b)

configs = Configs()

