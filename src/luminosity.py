from PIL import Image, ImageDraw

# Change this... should bet between -255 and +255
# negative numbers dim, positive numbers brighten
luminosity = -80

# Load image:
input_image = Image.open("img/vaccines.png")
input_pixels = input_image.load()

# Create output image
output_image = Image.new("RGB", input_image.size)
draw = ImageDraw.Draw(output_image)

print (input_pixels[0, 0])

# Generate image
for x in range(output_image.width):
  for y in range(output_image.height):
    (r, g, b, a) = input_pixels[x, y]
    r = int(r + luminosity)
    g = int(g + luminosity)
    b = int(b + luminosity)
    ## print (r, g, b)
    draw.point((x, y), (r, g, b))

output_image.save("img/luminous.png")
