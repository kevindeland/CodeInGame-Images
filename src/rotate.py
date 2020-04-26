from PIL import Image, ImageDraw
from math import sin, cos, pi

# Load image:
input_image = Image.open("img/vaccines.png")
input_pixels = input_image.load()

# Create output image
output_image = Image.new("RGB", input_image.size)
draw = ImageDraw.Draw(output_image)

angle = pi / 3 # angle in radians (what is the angle??)
center_x = input_image.width / 2
center_y = input_image.height / 2

### The Math
### xp = (x-cx) * cos(angle) - (y-cy) * sin(angle) + cx
### yp = (x-cx) * sin(angle) + (y-cy) * cos(angle) + cy
### I'm not sure I understand how this works or what it means...
### I suspect it has to do something with a matrix transformation?

# Copy pixels
for x in range(input_image.width):
  for y in range(input_image.height):
    # Compute coordinate in input image
    xp = int( (x - center_x) * cos(angle) - (y - center_y) * sin(angle) + center_x)
    yp = int( (x - center_x) * sin(angle) + (y - center_y) * cos(angle) + center_y)
    if 0 <= xp < input_image.width and 0 <= yp < input_image.height:
      draw.point((x, y), input_pixels[xp, yp])

output_image.save("img/rotated.png")
