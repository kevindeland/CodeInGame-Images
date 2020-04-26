from PIL import Image, ImageDraw
from numpy import dot

# Load image
input_image = Image.open("img/panamacity.jpg")
input_pixels = input_image.load()

# Box Blur kernel
# matrix stuff...
# [1] * 3 => [1, 1, 1]
# [[1, 1, 1]] * 3 => 3x3 matrix of 1s
# dot(x, 1/9) multiplies all elements of x by 1/9
box_size = 7 ## must be odd
box_kernel = dot([[1] * box_size] * box_size, 1/(box_size **2))

# Gaussian kernel
gaussian_kernel = dot([
  [1,  4,  6,  4, 1],
  [4, 16, 24, 16, 4],
  [6, 24, 36, 24, 6],
  [4, 16, 24, 16, 4],
  [1,  4,  6,  4, 1]
], 1/256)

# Select kernel here
kernel = box_kernel

# Middle of kernel
offset = len(kernel) // 2
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
        xn = x + a - offset  ## this is the x,y value of the pixel we're observing
        yn = y + b - offset
        pixel = input_pixels[xn, yn]
        acc[0] += pixel[0] * kernel[a][b] ## red
        acc[1] += pixel[1] * kernel[a][b] ## green
        acc[2] += pixel[2] * kernel[a][b] ## blue

    draw.point((x, y), (int(acc[0]), int(acc[1]), int(acc[2])))

output_image.save("img/blurred_box_7.jpg")
