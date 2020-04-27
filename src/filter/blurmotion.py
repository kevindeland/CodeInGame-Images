from PIL import Image, ImageDraw
from numpy import dot
from math import pi, cos, sin, degrees

# Load image
## input_image = Image.open("img/pittsburgh.jpg")
input_image = Image.open("img/patchwork_big.png")
input_pixels = input_image.load()

# Motion Blur kernel
angle = pi /2 ## vertical
## angle = 0 ## horizontal
motion_size = 3 ## must be odd
motion_kernel = dot([1] * motion_size, 1/(motion_size))
motion_kernel_angle = dot([
  [  0, sin(angle), 0],
  [cos(angle), 1, cos(angle)],
  [  0, sin(angle), 0]
], 1/3)

  
# Select kernel here
kernel = motion_kernel_angle
print(kernel)
print (len(kernel))

# Middle of kernel
offset = motion_size // 2
print(offset)

# Create output image
output_image = Image.new("RGB", input_image.size)
draw = ImageDraw.Draw(output_image)

# Compute convolution (??) between intensity (??) and kernels
for x in range(offset, input_image.width - offset):
  for y in range(offset, input_image.height - offset):
    acc = [0, 0, 0] ## accumulator
    for a in range(len(kernel)): ## iterate through each cell within the kernel
      for b in range(len(kernel)):
        xn = x + b - offset  ## this is the x,y value of the pixel we're observing
        yn = y + a - offset
        pixel = input_pixels[xn, yn]
        acc[0] += pixel[0] * kernel[a][b] ## red
        acc[1] += pixel[1] * kernel[a][b] ## green
        acc[2] += pixel[2] * kernel[a][b] ## blue

    draw.point((x, y), (int(acc[0]), int(acc[1]), int(acc[2])))

## output_image.save("img/blur/motion/patchwork_" + str(motion_size) + ".png")
output_image.save("img/blur/motion/angle/patchwork_" + str(int(degrees(angle))) + ".png")
