### from here:
## https://www.pyimagesearch.com/2014/05/26/opencv-python-k-means-color-clustering/

# import packages
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import argparse
import utils
import cv2

from PIL import ImageDraw, Image

# construct argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
ap.add_argument("-c", "--clusters", required=True, type=int, help="# of clusters")
ap.add_argument("-o", "--output", required=True, help="Path to the output")
args = vars(ap.parse_args())

# load image and convert it from BGR to RGB so
# we can display it with matplotlib
image = cv2.imread(args["image"])
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

## switching between cv2 and PIL
output_image = Image.new("RGB", (image.shape[1], image.shape[0]))
draw = ImageDraw.Draw(output_image)

## image is now a list of pixels
pixel_array = image.reshape((image.shape[0] * image.shape[1], 3)) 

# print("Here's the image dimensions and shit")
# print(image.shape[1], image.shape[0])

# cluster the pixel intensities
clt = KMeans(n_clusters = args["clusters"])
clt.fit(pixel_array)

# print("This is an array of (r,g,b) pixels classified by their cluster")
# print(clt)
# print(clt.labels_)

print(args["image"])

for c in clt.cluster_centers_:
    print ('{r:', round(c[0]), ', g:', round(c[1]), 'b:', round(c[2]), '}')
## print(clt.cluster_centers_)

### How can we filter out the black / empty ones???

## build a histogram of clusters and then create a figure
## representing the number of pixels labeled to each other
hist = utils.centroid_histogram(clt)
bar = utils.plot_colors(hist, clt.cluster_centers_)

for x in range(output_image.width):
    for y in range(output_image.height):

        index = y * output_image.width + x
        ## print(index)
        label = clt.labels_[index]
        pixel = clt.cluster_centers_[label]
        ## print(pixel)
        draw.point((x, y), (int(pixel[0]), int(pixel[1]), int(pixel[2])))


# show image
output_image.save(args["output"])

import sys
sys.exit()

fig1 = plt.figure(1)
plt.axis("off")
plt.imshow(image)
fig1.show()


# show color bart
fig2 = plt.figure(2)
plt.axis("off")
plt.imshow(bar)
fig2.show()

input()

        
