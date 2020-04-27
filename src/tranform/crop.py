from PIL import Image, ImageDraw
from math import floor

# Load image:
input_image = Image.open("img/headshot.png")
input_pixels = input_image.load()

print(input_image.width, input_image.height)


### do little sections
section_size = 100
sections_x = floor(input_image.width / section_size)
sections_y = floor(input_image.height / section_size)

for i in range(sections_x):
  for j in range(sections_y):
    # Cropped area
    x_origin = i*section_size
    y_origin = j*section_size
    origin = (x_origin, y_origin)
    end = (x_origin + section_size, y_origin + section_size)

    # Create output image of size (w, h) where (w = end[0] - origin[0]), h = ...
    output_image = Image.new("RGB", (end[0] - origin[0], end[1] - origin[1]))
    draw = ImageDraw.Draw(output_image)

    # Copy pixels
    for x in range(output_image.width):
      for y in range(output_image.height):
        xp, yp = x + origin[0], y + origin[1]
        draw.point((x, y), input_pixels[xp, yp])

    output_image.save("img/crop/kevin_" + str(i) + "_" + str(j) + ".png")
    print("saved image", i, j)
