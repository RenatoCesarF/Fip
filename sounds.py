import pygame


class Sounds:
    favorite: pygame.mixer.Sound
    rotate: pygame.mixer.Sound
    passing: pygame.mixer.Sound
    trash: pygame.mixer.Sound

    @classmethod
    def load(cls) -> None:
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        cls.favorite = pygame.mixer.Sound("./assets/favorite.ogg")
        cls.rotate = pygame.mixer.Sound("./assets/rotate.ogg")

        cls.passing = pygame.mixer.Sound("./assets/pass.ogg")
        cls.trash = pygame.mixer.Sound("./assets/trash.ogg")

        for attribute in vars(cls).values():
            set_volume = getattr(attribute, "set_volume", None)

            if callable(set_volume):
                set_volume(0.3)
