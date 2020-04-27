from PIL import Image, ImageDraw
from numpy import dot

# Load image
input_image = Image.open("img/pittsburgh.jpg")
input_pixels = input_image.load()

### Unsharp mask
# subtract from original image a *mask* created using a low-pass filter (box kernel)
# removes the "blurry" part of the image
# sharpened = original + (original - blurred) * amount
# how???

# Low-pass kernel
kernel = dot([[1] * 3] * 3, 1/(3**2))

amount = 3

# Middle of the kerenl
offset = len(kernel) // 2

# Create output image
output_image = Image.new("RGB", input_image.size)
draw = ImageDraw.Draw(output_image)

# Compute convolution with kernel
for x in range(offset, input_image.width - offset):
  for y in range(offset, input_image.height - offset):
    original_pixel = input_pixels[x, y]
    acc = [0, 0, 0]
    for a in range(len(kernel)):
      for b in range(len(kernel)):
        xn = x + a - offset
        yn = y + b - offset
        pixel = input_pixels[xn, yn]
        acc[0] += pixel[0] * kernel[a][b]
        acc[1] += pixel[1] * kernel[a][b]
        acc[2] += pixel[2] * kernel[a][b]

    new_pixel = (
      int(original_pixel[0] + (original_pixel[0] - acc[0]) * amount),
      int(original_pixel[1] + (original_pixel[1] - acc[1]) * amount),
      int(original_pixel[2] + (original_pixel[2] - acc[2]) * amount)
    )
    draw.point((x, y), new_pixel)

output_image.save("img/sharpen/unsharpened" + str(amount) + ".jpg")
