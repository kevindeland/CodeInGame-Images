from PIL import Image, ImageDraw
from math import sqrt

# Load image:
input_image = Image.open("img/juggle.jpg")
input_pixels = input_image.load()

# Sobel kernels
kernely = [[-1, 0, 1],
           [-2, 0, 2],
           [-1, 0, 1]]
kernelx = [[-1, -2, -1],
           [0, 0, 0],
           [1, 2, 1]]

# Create output image
output_image = Image.new("RGB", input_image.size)
draw = ImageDraw.Draw(output_image)

# Compute convolution between intensity and kernels
for x in range(1, input_image.width - 1):
  for y in range(1, input_image.height - 1):
    magx, magy = 0, 0
    for a in range(3):
      for b in range(3):
        xn = x + a - 1
        yn = y + b - 1
        intensity = sum(input_pixels[xn, yn]) / 3
        magx += intensity * kernelx[a][b]
        magy += intensity * kernely[a][b]

    # Draw in black and white the magnitude
    color = int(sqrt(magx**2 + magy**2))
    draw.point((x, y), (color, color, color))

output_image.save("img/juggle_sobel.jpg")
