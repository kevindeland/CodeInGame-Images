from PIL import Image, ImageDraw

# Load image:
input_image = Image.open("img/headshot.png")
input_pixels = input_image.load()

# Create output image (vertical flip)
output_image_vertical = Image.new("RGB", input_image.size)
draw_vertical = ImageDraw.Draw(output_image_vertical)

# Create output image (horizontal flip)
output_image_horizontal = Image.new("RGB", input_image.size)
draw_horizontal = ImageDraw.Draw(output_image_horizontal)

output_image_both = Image.new("RGB", input_image.size)
draw_both = ImageDraw.Draw(output_image_both)

# Copy pixels
# (can loop over horizontal flip dimensions for both, b/c they're the same)
for x in range(output_image_horizontal.width):
  for y in range(output_image_horizontal.height):
    xp = input_image.width - x - 1
    yp = input_image.height - y - 1
    draw_horizontal.point((x, y), input_pixels[xp, y])
    draw_vertical.point((x, y), input_pixels[x, yp])
    draw_both.point((x, y), input_pixels[xp, yp])


output_image_horizontal.save("img/flipped_h.png")
output_image_vertical.save("img/flipped_v.png")
output_image_both.save("img/flipped_both.png")
