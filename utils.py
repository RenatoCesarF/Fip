import os

def correct_image_name(og):
    new_name = og
    # if og.endswith(".JPG.JPG"):
    #     new_name = og[:len(og)-4]
    if og.startswith("._"):
        new_name = new_name[2:]
    return new_name


def copy_only_images(current_dir, items):
    ignored_items = []
    allowed_extensions = {'.png', '.jpg', '.jpeg'}
    
    for item in items:
        full_path = os.path.join(current_dir, item)
        # Only evaluate if it is a file
        if os.path.isfile(full_path):
            _, ext = os.path.splitext(item)
            if ext.lower() not in allowed_extensions:
                ignored_items.append(item)
                
    return ignored_items
