### The contrast is the difference in brightness (or color) that makes the objects in a picture distinguishable. The intensity histogram of an image is the distribution of pixel luminance for an image. In order to improve the contrast, we can use a linear normalization of the intensity histogram:

## I_normalized = (I_this - I_min) * 255 / (I_max - I_min)

## Wait wtf... an image with pure black and pure white won't change!!!
## I_max = 255, I_min = 0, so the equation is just (I_this - 0) * 255 / (255 - 0) ==> I_this


from PIL import Image, ImageDraw

# Load image:
input_image = Image.open("img/chameleon.jpg")
input_pixels = input_image.load()

# Create output image
output_image = Image.new("RGB", input_image.size)
draw = ImageDraw.Draw(output_image)

# let's see if this changes anything?
contrast = 255
# hmmmm if it's 0 it should go to gray (127), not black (0)!
# okay subtracting the mean didn't work...
# to figure this out, we might have to run some simulations... maybe later!
# well... it does something!!!
## https://www.dfstudios.co.uk/articles/programming/image-programming-algorithms/image-processing-algorithms-part-5-contrast-adjustment/
## Try this link

# Find minimum and maximum luminosity
imin = 255
imax = 0
for x in range(input_image.width):
  for y in range(input_image.height):
    (r, g, b) = input_pixels[x, y]
    i = (r + g + b) / 3
    imin = min(imin, i)
    imax = max(imax, i)

print (imin, imax)

imean = (imax - imin) / 2
print (imean)

# Generate image
for x in range(output_image.width):
  for y in range(output_image.height):
    (r, g, b) = input_pixels[x, y]
    # Current luminosity
    i = (r + g + b) / 3
    # New luminosity
    ip = contrast * (i - imin) / (imax - imin) ## + imean
    r = int(r * ip/i)
    g = int(g * ip/i)
    b = int(b * ip/i)
    draw.point((x, y), (r, g, b))

output_image.save("img/contrasted.jpg")
