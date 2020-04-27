from PIL import Image, ImageDraw

# Spectrum of luminosity, from x=0 to x=width
lum = (255, -255)

# Load image:
input_image = Image.open("img/chameleon.jpg")
input_pixels = input_image.load()

# Create output image
output_image = Image.new("RGB", input_image.size)
draw = ImageDraw.Draw(output_image)

# Generate image
for x in range(output_image.width):
  for y in range(output_image.height):
    (r, g, b) = input_pixels[x, y]
    ## L = mx+b
    ## m = (lum[1] - lum[0]) / width
    ## b = lum[0]
    l_scaled = (lum[1] - lum[0]) * x / output_image.width + lum[0]
    r = int(r + l_scaled)
    g = int(g + l_scaled)
    b = int(b + l_scaled)
    ## print (r, g, b)
    draw.point((x, y), (r, g, b))

output_image.save("img/luminosity/luminx_" + str(lum[0]) + "_" + str(lum[1]) + ".jpg")
