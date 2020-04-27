from PIL import Image, ImageDraw

### write (rp, gp, bp) to be (ip)
### where ip = (r + g + b) / 3

# Load image
input_image = Image.open("img/chameleon.jpg")
input_pixels = input_image.load()

# Create output image
output_image = Image.new("RGB", input_image.size)
draw = ImageDraw.Draw(output_image)

# Generate image
for x in range(output_image.width):
  for y in range(output_image.height):
    (r, g, b) = input_pixels[x, y]
    ip = int((r + g + b) / 3)
    draw.point((x, y), (ip, ip, ip))

# Save image
output_image.save("img/grayscaled.jpg")
