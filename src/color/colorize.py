from PIL import Image, ImageDraw
import argparse

parser = argparse.ArgumentParser(description='Change colors in an image')
parser.add_argument('-i', metavar='i', type=str, nargs=1, help='the input file', required=True)
parser.add_argument('-o', metavar='o', type=str, nargs=1, help='the output file', required=True)
parser.add_argument('-t', metavar='t', type=int, nargs=1, help='the threshold', default=[200])

parser.add_argument('-r', metavar='r', type=int, nargs=1, help='red value')
parser.add_argument('-g', metavar='g', type=int, nargs=1, help='green value')
parser.add_argument('-b', metavar='b', type=int, nargs=1, help='blue value')
args = parser.parse_args()

filein = args.i[0]
filetype = filein.split('.')[1]

color_target = None
if(args.r != None and
   args.g != None and
   args.b != None):
  r_tar= args.r[0]
  g_tar= args.g[0]
  b_tar= args.b[0]
  color_target = (r_tar, g_tar, b_tar)


# Square distance between 2 colors
def distance2(c1, c2):
  r1, g1, b1 = c1
  if filetype == "png":
    r2, g2, b2, a = c2 ## if png
  elif filetype == "jpg":
    r2, g2, b2 = c2 ## if jpg
  return (r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2

## WHOA! can we change this to something else?

color_key = 'magenta'
colors = {
  'blue': (0, 0, 255),
  'green': (0, 255, 0),
  'red': (255, 0, 0),
  'magenta': (255, 0, 255),
  'cyan': (0, 255, 255),
  'yellow': (255, 255, 0)
}
birds = {
  'flowers': (165, 84, 99),
  'bodies': (154, 148, 195),
  'wings': (87, 80, 130),
  'beaks': (225, 214, 132),
  'branches': (84, 186, 174),
  'leaves': (66, 101, 72)
}
geometry = {
  'void': (11, 17, 31),
  'floor': (53, 225, 255),
  'septagon': (251, 1, 251),
  'pyramid': (112, 237, 87),
  'dodec': (253, 195, 105)
}
color_to_change =  geometry['dodec'] # birds['bodies'] #color_target if color_target is not None else colors[color_key]

scalar_key = 'red'
scalars = {
    'green': (0.5, 1.25, 0.5),
    'blue': (0.5, 0.5, 1.25),
    'red': (1.25, 0.5, 0.5),
    'yellow': (1.25, 1.25, 0.5),
    'cyan': (0.5, 1.25, 1.25),
    'magenta': (1.25, 0.5, 1.25)
}

scalar = scalars[scalar_key]

constants = {
  'black': (0, 0, 0)
}

threshold = args.t[0]

# Load image
input_image = Image.open(args.i[0])
input_pixels = input_image.load()

# Create output image
output_image = Image.new("RGB", input_image.size)
draw = ImageDraw.Draw(output_image)

# Generate image
for x in range(output_image.width):
  for y in range(output_image.height):
    if filetype == "png":
      (r, g, b, a) = input_pixels[x, y] ## png
    elif filetype == "jpg":
      (r, g, b) = input_pixels[x, y] ## jpg
    if distance2(geometry['dodec'], input_pixels[x, y]) < threshold ** 2:
      scalar = scalars['red']
      r = int(r * scalar[0])
      g = int(g * scalar[1])
      b = int(b * scalar[2])
      draw.point((x, y), (r, g, b))
    elif distance2(geometry['septagon'], input_pixels[x, y]) < threshold ** 2:
      s2 = scalars['yellow']
      r = int(r * s2[0])
      g = int(g * s2[1])
      b = int(b * s2[2])
      draw.point((x, y), (r, g, b))
    else:
      draw.point((x, y), input_pixels[x, y])

# Save image
output_image.save(args.o[0])
print("Wrote new image to", args.o[0])
