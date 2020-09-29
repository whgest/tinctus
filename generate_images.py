import os
import numpy
from dataclasses import dataclass
from PIL import Image

INPUT_DIR = "in"
OUTPUT_DIR = "out"
PALETTE_DIR = "palette"


@dataclass(eq=True, frozen=True)
class Color:
    red: int = 0
    green: int = 0
    blue: int = 0


@dataclass(eq=True, frozen=True)
class Swap:
    old: Color
    new: Color


def diff_images(original_palette: Image, recolor_palette: Image):
    """
    Compare palettes and map color swaps for later use
    """
    original = numpy.array(original_palette)
    recolor = numpy.array(recolor_palette)

    assert original_palette.width == recolor_palette.width, "Original and recolor palette files are different widths."

    swaps = []

    for h in range(1):
        for w in range(original_palette.width):

            if numpy.array_equal(original[h][w], recolor[h][w]):
                continue
            else:
                red = original[h][w][0]
                green = original[h][w][1]
                blue = original[h][w][2]

                red2 = recolor[h][w][0]
                green2 = recolor[h][w][1]
                blue2 = recolor[h][w][2]
                swaps.append(Swap(Color(red, green, blue), Color(red2, green2, blue2)))
                swaps = list(set(swaps))

    return swaps


def create_layer_images(changes_only=True):
    """
    Perform color conversion swaps on all files in INPUT_DIR
    :param changes_only: Creates layer images with only changed pixels. Renders complete image is False.
    """
    with Image.open(os.path.join(PALETTE_DIR, 'original.png')) as original:
        with Image.open(os.path.join(PALETTE_DIR, 'recolor.png')) as recolor:
            swaps = diff_images(original, recolor)

    for image_file in os.listdir(INPUT_DIR):
        _, file_extension = os.path.splitext(image_file)
        if file_extension != ".png":
            continue

        with Image.open(os.path.join(INPUT_DIR, image_file)) as im:
            in_data = numpy.array(im)
            if changes_only:
                out_data = numpy.zeros([39, 39, 4], dtype=numpy.uint8)
            else:
                out_data = numpy.array(im)

            red, green, blue, alpha = in_data.T

            for swap in swaps:
                to_change = (red == swap.old.red) & (blue == swap.old.blue) & (green == swap.old.green)
                out_data[...][to_change.T] = (swap.new.red, swap.new.green, swap.new.blue, 255)

            im2 = Image.fromarray(out_data)

            im2.save(os.path.join(OUTPUT_DIR, image_file))


create_layer_images()
