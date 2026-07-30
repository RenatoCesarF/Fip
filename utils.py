import pygame
# def write(screen, text, pos, color):
#     text_surface = font.render(text, True, color)
#     screen.blit(text_surface, pos)


def fill(surface, color):
    """Fill all pixels of the surface with color, preserve transparency."""
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))

def correct_image_name(og):
    new_name = og
    # if og.endswith(".JPG.JPG"):
    #     new_name = og[:len(og)-4]
    if og.startswith("._"):
        new_name = new_name[2:]
    return new_name

