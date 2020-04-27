from PIL import Image, ImageDraw

# Square distance between 2 colors
def distance2(c1, c2):
  r1, g1, b1 = c1
  r2, g2, b2, a = c2
  return (r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2

## WHOA! can we change this to something else?

color_key = 'blue'
colors = {
  'blue': (0, 0, 255),
  'green': (0, 255, 0),
  'red': (255, 0, 0)
}
color_to_change = colors[color_key]

scalar_key = 'red'
scalars = {
    'green': (0.5, 1.25, 0.5),
    'blue': (0.5, 0.5, 1.25),
    'red': (1.25, 0.5, 0.5)
}
scalar = scalars[scalar_key]

threshold = 200

# Load image
input_image = Image.open("img/colorwheel.png")
input_pixels = input_image.load()

# Create output image
output_image = Image.new("RGB", input_image.size)
draw = ImageDraw.Draw(output_image)

# Generate image
for x in range(output_image.width):
  for y in range(output_image.height):
    (r, g, b, a) = input_pixels[x, y]
    if distance2(color_to_change, input_pixels[x, y]) < threshold ** 2:
      r = int(r * scalar[0])
      g = int(g * scalar[1])
      b = int(b * scalar[2])
    draw.point((x, y), (r, g, b))

# Save image
output_image.save("img/colorized/b2r/wheel_" + str(threshold) + ".png")
