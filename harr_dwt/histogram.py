import matplotlib.pyplot as plt
import cv2

# im = cv2.imread('mountain.jpg')
im = cv2.imread('watermarked.jpeg')
# calculate mean value from RGB channels and flatten to 1D array
vals = im.mean(axis=2).flatten()
# plot histogram with 255 bins
b, bins, patches = plt.hist(vals, 255)
plt.xlim([0,255])
plt.show()