from PIL import Image, ImageDraw
from numpy import dot
from math import pi, cos, sin

# Load image
## input_image = Image.open("img/pittsburgh.jpg")
input_image = Image.open("img/patchwork_big.png")
input_pixels = input_image.load()

# Motion Blur kernel
angle = pi /2 ## vertical
## angle =  ## horizontal
motion_size = 9 ## must be odd
motion_kernel = dot([1] * motion_size, 1/(motion_size))
motion_kernel_angle = dot([
  [  0, sin(angle), 0],
  [cos(angle), 1, cos(angle)],
  [  0, sin(angle), 0]
], 1/3)
  
# Select kernel here
kernel = motion_kernel

# Middle of kernel
offset = motion_size // 2
print(offset)

# Create output image
output_image = Image.new("RGB", input_image.size)
draw = ImageDraw.Draw(output_image)

# Compute convolution (??) between intensity (??) and kernels
for x in range(offset, input_image.width - offset):
  for y in range(0, input_image.height):
    acc = [0, 0, 0] ## accumulator
    for a in range(len(kernel)): ## iterate through each cell within the kernel
      xn = x + a - offset  ## this is the x,y value of the pixel we're observing
      pixel = input_pixels[xn, y]
      acc[0] += pixel[0] * kernel[a] ## red
      acc[1] += pixel[1] * kernel[a] ## green
      acc[2] += pixel[2] * kernel[a] ## blue

    draw.point((x, y), (int(acc[0]), int(acc[1]), int(acc[2])))

output_image.save("img/blur/motion/patchwork_" + str(motion_size) + ".png")
## output_image.save("img/blur/motion/angle/patchwork_" + str(angle) + ".png")
