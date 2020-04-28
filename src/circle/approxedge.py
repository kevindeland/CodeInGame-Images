from PIL import Image, ImageDraw
import numpy as np
from math import sqrt

# Load image
input_image = Image.open("img/juggle.jpg")
input_pixels = input_image.load()
width, height = input_image.width, input_image.height

# Create output image
output_image = Image.new("RGB", input_image.size)
draw = ImageDraw.Draw(output_image)

# Convert to grayscale
intensity = np.zeros((width, height))
for x in range(width):
  for y in range(height):
    ## two colors can have a very similar intensity but look very different (e.g. red and blue)
    intensity[x, y] = sum(input_pixels[x, y]) / 3 ## average the rgb values

# Compute convolution between intensity and kernels
for x in range(1, input_image.width - 1):
  for y in range(1, input_image.height - 1):
    magx = intensity[x+1, y] - intensity[x-1, y] ## difference between left and right pixel
    magy = intensity[x, y+1] - intensity[x, y-1] ## difference between top and bottom pixel

    # Draw magnitude in black and white
    color = int(sqrt(magx**2 + magy**2))
    draw.point((x, y), (color, color, color))

output_image.save("img/juggle_approx.jpg")
