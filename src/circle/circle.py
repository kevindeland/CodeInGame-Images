from PIL import Image, ImageDraw
from math import sqrt, pi, cos, sin
from canny import canny_edge_detector
from collections import defaultdict
from argparse import ArgumentParser as AP
from sys import exit

parser = AP(description='Find circles in an image')
parser.add_argument('-i', metavar='i', type=str, nargs=1, help='the input file', required=True)
parser.add_argument('-o', metavar='o', type=str, nargs=1, help='the output file', required=True)
parser.add_argument('--rmin', metavar='rmin', type=int, nargs=1, help='rmin', default=[18])
parser.add_argument('--rmax', metavar='rmax', type=int, nargs=1, help='rmax', default=[20])
parser.add_argument('--threshold', metavar='threshold', type=float, nargs=1, help='threshold', default=[0.4])
args = parser.parse_args()

# Load image:
input_image = Image.open(args.i[0])

# Output image:
output_image = Image.new("RGB", input_image.size)
output_image.paste(input_image)
draw_result = ImageDraw.Draw(output_image)

# Find circles (could change these...)
rmin = args.rmin[0]
rmax = args.rmax[0]
steps = 100
threshold = args.threshold[0]

## points is our "radial kernel"
points = []
for r in range(rmin, rmax + 1):
  for t in range(steps):
    points.append((r,
                   int(r * cos(2*pi * t/steps)),
                   int(r * sin(2*pi * t/steps))))


# print(points)
# exit()

acc = defaultdict(int)
for x, y in canny_edge_detector(input_image):
  for r, dx, dy in points:
    a = x - dx
    b = y - dy
    acc[(a, b, r)] += 1

## print(acc.items())
## exit()

sorted_items = sorted(acc.items(), key=lambda i: -i[1])

## print(sorted_items)
## exit()

circles = []
for k, v in sorted(acc.items(), key=lambda i: -i[1]):
  x, y, r = k
  if v/steps >= threshold and all((x-xc)**2 + (y-yc)**2 > rc**2 for xc, yc, rc in circles):
    print(v/steps, x, y, r)
    circles.append((x, y, r))

print(circles)
for x, y, r in circles:
  pad = 8
  ##draw_result.ellipse((x-r, y-r, x+r, y+r), outline=(255,0,0,0))
  
  draw_result.ellipse((x-r-pad, y-r-pad, x+r+pad, y+r+pad), outline=(255,255,255,0), width=4)

# Save output image
output_image.save(args.o[0])
print("Saved to file", args.o[0])
