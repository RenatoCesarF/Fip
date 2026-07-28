def correct_image_name(og):
    new_name = og
    if og.endswith(".JPG.JPG"):
        new_name = og[:len(og)-4]
    if og.startswith("._"):
        new_name = new_name[2:]
    return new_name

