# Pillow image tutorials
Based on tutorials [here](https://www.codingame.com/playgrounds/2524/basic-image-manipulation/introduction)

## Transformations

### crop.py
1. Crop an image √√√
2. Crop an image into tiny images of 100x100 √√√

### scale.py
1. Scale an image (omg it looks so pixely, I love it) √√√

### flip.py
1. can flip an image across horizontal and/or vertical axis √√√

### rotate.py
1. can rotate about the center (not sure how this works. See inline comments for details). What's the math behind this???


## Colors

### Luminosity
1. Dim or brighten an image √√√
2. Luminosity as function of position in image √√√

### Contrast
- The contrast is the difference in brightness that makes the objects in an image distinguishable. See inline comments for more.
- Check out this resource for more info on a [real contrast algorithm](https://www.dfstudios.co.uk/articles/programming/image-programming-algorithms/image-processing-algorithms-part-5-contrast-adjustment/).

### Colorize!!!
I hope this is cool... "In the next example, we detect the pixels whose color is close to blue (0, 0, 255) by computing a distance, and we reduce the value of the red and blue components and increase the green component. What will this look like? Anything blue will become less blue, less red, and more green.

Try going in and changing the references `color_to_change = colors['green']` and `scalar = scalars['red']`.

It is really fun to experiment with the **color wheel** images and change the threshold.

#### Grayscale
1. Set all the pixel RGB values to their intensity


## Filtering

### Blur
1. box kernel (experiment w/ different sizes, make sketches of how it works)
2. gaussian kernel

![how box kernel works](./illustrations/box_kernel.png)

### Sharpening
1. use a high pass filter to boost pixels when the neighbor pixels are different
2. unsharp mask: remove the blurry part of the image (look at the difference in any of the building windows in the Pittsburgh image)

### Edge detection
1. Sobel Operator: uses two kernels (horizontal, vertical) to detect edges. It works great!


## Circle Detection
See tutorials [here](https://www.codingame.com/playgrounds/38470/how-to-detect-circles-in-images).

### Edge detection
(?)

### Sobel operator
already done as part of first tutorial

### Canny Algorithm
Follow these steps
1. *Gaussian filter* - smooths the image to remove noise.
2. Compute image gradient - identifies the edges
3. Non-maximum suppression - compute the direction of the gradient, and remove pixels that are not the maximum among their neighbors (??? what does this mean ???)
4. Edge tracking - track edges by strength (low, high, and in-between)

### Circle Hough Transform
Circle equation:
```
x = a + r*cos(t);
y = b + r*sin(t);
t within [0, 2π);
```

Using the edges from our Canny edge detector and for each possible circle, we count the nuber of edges that are a part of each circle.

**YES!!!**
This seems to work best:
```
python3 src/circle/circle.py -i img/inputs/juggle.jpg -o img/circles/juggle_circles.jpg --rmin 14 --rmax 16 --threshold=0.5
```
It gets all six balls, and nothing else! (cheating)