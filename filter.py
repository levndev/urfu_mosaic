import argparse
import numpy as np
from PIL import Image


def crop_img(pixels, distance):
    height_overflow = len(pixels) % distance
    width_overflow = len(pixels[1]) % distance
    return pixels[:len(pixels) - height_overflow,
                  :len(pixels[0]) - width_overflow]


parser = argparse.ArgumentParser()
parser.add_argument("input", type=str, help="path to image")
parser.add_argument("--output", dest="output", type=str, help="path to result image", default="res.jpg")
parser.add_argument("--size", dest="size", type=int, help="mozaik size", default=10)
parser.add_argument("--gradations", dest="gradation_count", type=int, help="How many gray gradations will be in result image", default=4)
args = parser.parse_args()

img = Image.open(args.input)
mosaic_size = args.size
gradation = args.gradation_count
res_file = args.output

pixels = np.array(img)
gradation_step = 256 / gradation

pixels = crop_img(pixels, mosaic_size)
height = len(pixels)
width = len(pixels[1])

for x in range(0, width - mosaic_size+1, mosaic_size):
    for y in range(0, height - mosaic_size+1, mosaic_size):
        mosaic = pixels[y:y + mosaic_size, x:x + mosaic_size]
        average = np.average(mosaic)
        average = int(average//gradation_step) * gradation_step
        mosaic.fill(average)

res = Image.fromarray(pixels)
res.save(res_file)