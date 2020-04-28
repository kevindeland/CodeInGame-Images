from math import sqrt, atan2, pi
import numpy as np
import sys

##
## export this function
## calls sequence of other functions
##
def canny_edge_detector(input_image):
  input_pixels = input_image.load()
  w = input_image.width
  h = input_image.height

  # Transform the image to grayscale
  grayscaled = compute_grayscale(input_pixels, w, h, False)

  # Blur grayscale to remove noise
  blurred = compute_blur(grayscaled, w, h, False)

  # Compute the gradient
  gradient, direction = compute_gradient(blurred, w, h, False)

  # Non-maximum suppression
  filter_out_non_maximum(gradient, direction, w, h)

  # Filter out some edges
  keep = filter_strong_edges(gradient, w, h, 20, 25) ## what are these numbers for??

  return keep

##
## retuns a w*h array of pixels (grayscale)
##
def compute_grayscale(input_pixels, width, height, save):
  print("computing grayscale")
  grayscale = np.empty((width, height))
  for x in range(width):
    for y in range(height):
      pixel = input_pixels[x, y]
      grayscale[x, y] = (pixel[0] + pixel[1] + pixel[2]) / 3

  if save:
    output_image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(output_image)
    for x in range(width):
      for y in range(height):
        i = int(grayscale[x, y])
        draw.point((x, y), (i, i, i))
        
    output_image.save("img/canny/gray_juggle.jpg")

  print("finished grayscale")
  return grayscale
##

##
## retuns a w*h array of pixels (blurred)
##
def compute_blur(input_pixels, width, height, save):
  print("computing blur")
  # Keep coordinate inside image
  # I guess it... returns x only if it's inside the boundaries (how does this work with accumulator?)
  clip = lambda x, l, u: l if x < l else u if x > u else x

  # Gaussian kernel
  kernel = np.array([
      [1 / 256,  4 / 256,  6 / 256,  4 / 256, 1 / 256],
      [4 / 256, 16 / 256, 24 / 256, 16 / 256, 4 / 256],
      [6 / 256, 24 / 256, 36 / 256, 24 / 256, 6 / 256],
      [4 / 256, 16 / 256, 24 / 256, 16 / 256, 4 / 256],
      [1 / 256,  4 / 256,  6 / 256,  4 / 256, 1 / 256]
  ])

  # Middle of the kernel
  offset = len(kernel) // 2

  # Compute the blurred image
  blurred = np.empty((width, height))
  for x in range(width):
    for y in range(height):
      acc = 0
      for a in range(len(kernel)):
        for b in range(len(kernel)):
          xn = clip(x + a - offset, 0, width - 1)
          yn = clip(y + b - offset, 0, height - 1)
          acc += input_pixels[xn, yn] * kernel[a, b]
      blurred[x, y] = int(acc)

  if save:
    output_image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(output_image)
    for x in range(width):
      for y in range(height):
        i = int(blurred[x, y])
        draw.point((x, y), (i, i, i))
        
    output_image.save("img/canny/blur_juggle.jpg")
  
  print("finished blurred")
  return blurred

##
## gradient is ??
## direction is the direction of the edge???
## both are w*h arrays of pixels
##
def compute_gradient(input_pixels, width, height, save):
  print("computing gradient")
  gradient = np.zeros((width, height))
  direction = np.zeros((width, height))
  for x in range(width):
    for y in range(height):
      if 0 < x < width-1 and 0 < y < height-1:
        magx = input_pixels[x+1, y] - input_pixels[x-1, y]
        magy = input_pixels[x, y+1] - input_pixels[x, y-1]
        ## it looks like a negative?
        ### wtf, the guy's suit should be black
        gradient[x, y] = sqrt(magx**2 + magy**2)
        direction[x, y] = atan2(magy, magx) ## penicillin: when it's a negative, can emboss!!

  if save:
    g_output = Image.new("RGB", (width, height))
    g_draw = ImageDraw.Draw(g_output)
    d_output = Image.new("RGB", (width, height))
    d_draw = ImageDraw.Draw(d_output)
    for x in range(width):
      for y in range(height):
        if x%10 == 0 and y%10 == 0:
          print(direction[x, y])
        g = int(gradient[x, y])
        g_draw.point((x, y), (g, g, g))
        d = int((direction[x, y] + pi) * 128 / pi) ## this is too perfect... it looks embossed!!!
        d_draw.point((x, y), (d, d, d))

    g_output.save("img/canny/gradient_juggle.jpg")
    d_output.save("img/canny/direction_juggle.jpg")

  print("finished gradient")
  return gradient, direction

##
## wtf is this???
##
def filter_out_non_maximum(gradient, direction, width, height):
  for x in range(1, width - 1):
    for y in range(1, height - 1):
      ## makes it positive. or adds pi. (why pi??)
      ## I think it gives us the quadrant?
      angle = direction[x, y] if direction[x, y] >= 0 else direction[x, y] + pi
      rangle = round(angle / (pi/4))
      mag = gradient[x, y]
      
      ### here is the interesting part... 
      if ((rangle == 0 or rangle == 4) and (gradient[x-1, y] > mag or gradient[x + 1, y] > mag)
        or (rangle == 1 and (gradient[x-1, y-1] > mag or gradient[x+1, y+1] > mag))
        or (rangle == 2 and (gradient[  x, y-1] > mag or gradient[  x, y+1] > mag))
        or (rangle == 3 and (gradient[x+1, y-1] > mag or gradient[x-1, y+1] > mag))):
        gradient[x, y] = 0

##
## returns a list of edges to keep
## an edge is an (x,y) ??
##
def filter_strong_edges(gradient, width, height, low, high):
  # Keep strong edges
  keep = set()
  for x in range(width):
    for y in range(height):
      if gradient[x, y] > high:
        keep.add((x, y))

  # Keep weak edges if they're next to a pixel to keep
  lastiter = keep
  while lastiter:
    newkeep = set()
    for x, y in lastiter:
      for a, b in ((-1,-1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
        if gradient[x + a, y + b] > low and (x+a, y+b) not in keep:
          newkeep.add((x+a, y+b))
    keep.update(newkeep)
    lastiter = newkeep

  return list(keep)

if __name__ == "__main__":
  from PIL import Image, ImageDraw
  input_image = Image.open("img/inputs/juggle.jpg")
  output_image = Image.new("RGB", input_image.size)
  draw = ImageDraw.Draw(output_image)
  for x, y in canny_edge_detector(input_image):
    draw.point((x, y), (255, 255, 255))
  output_image.save("img/canny_lemons.jpg")



