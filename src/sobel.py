from PIL import Image, ImageDraw
from math import sqrt

# Load image
input_image = Image.open("img/patchwork_45.png")
input_pixels = input_image.load()

### Sobel Operator
# uses one kernel for each direction
# each kernel amplifies the difference, after converting to amplitude

# Calculate pixel intensity as average of rgb values
# (I didn't know you could do for loops like this in Python)
intensity = [[sum(input_pixels[x,y])/3 for y in range(input_image.height)] for x in range(input_image.width)]

# Sobel kernels
kernelx = [[-1, 0, 1],
           [-2, 0, 2],
           [-1, 0, 1]]
kernely = [[-1, -2, -1],
           [ 0,  0,  0],
           [ 1,  2,  1]]

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
        magx += intensity[xn][yn] * kernelx[a][b]
        magy += intensity[xn][yn] * kernely[a][b]

    # Draw in black and white the magnitude
    color = int(sqrt(magx**2 + magy**2))
    draw.point((x, y), (color, color, color))

output_image.save("img/edge/patchwork_45_sobel.png")
