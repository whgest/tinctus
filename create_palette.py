import os
import colorsys
import numpy
from PIL import Image

INPUT_DIR = "in"
PALETTE_DIR = "palette"

PALETTE_HEIGHT = 32


def print_palette_file():
    """
    Analyze all images in the input folder and create a palette PNG containing every color used therein, sorted by HSV
    """
    all_colors = []
    for image_file in os.listdir(INPUT_DIR):
        _, file_extension = os.path.splitext(image_file)
        if file_extension != ".png":
            continue
        with Image.open(os.path.join(INPUT_DIR, image_file)) as im:
            colors = im.getcolors(512)
            if not colors:
                print(f'{image_file} could not read colors.')
                continue
            all_colors.extend([c[1] for c in colors])

    color_values = list(set(all_colors))

    color_values.sort(key=lambda c: colorsys.rgb_to_hsv(c[0], c[1], c[2]))

    palette_colors = numpy.asarray([color_values] * PALETTE_HEIGHT).astype('uint8')

    palette_image = Image.fromarray(palette_colors, mode='RGBA')
    palette_image.save((os.path.join(PALETTE_DIR, 'original.png')))


print_palette_file()
