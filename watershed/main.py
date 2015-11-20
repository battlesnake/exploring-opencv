#!/usr/bin/python3

import numpy as np
import cv2 as cv

img_base_name = 'sample'
img_index = 0

def img_name(suffix):
    global img_index
    name = img_base_name
    if suffix:
        img_index = img_index + 1
        name = name + '-' + str(img_index) + '-' + suffix
    return name + '.jpg'

# Load image and rescale
original = cv.imread(img_name(0))
img = cv.resize(original, (1024, 768))
cv.imwrite(img_name('scale'), img)

# Get grayscale image for thresholding
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
cv.imwrite(img_name('thresh'), thresh)

# Noise removal
kernel = np.ones((3, 3), np.uint8)
opening = cv.morphologyEx(thresh, cv.MORPH_OPEN, kernel, iterations = 2)
cv.imwrite(img_name('opening'), opening)

# Definite background
sure_bg = cv.dilate(opening, kernel, iterations = 3)
cv.imwrite(img_name('sure_bg'), sure_bg)

# Definite foreground
dist_transform = cv.distanceTransform(opening, cv.DIST_L2, 5)
ret, sure_fg = cv.threshold(dist_transform, 0.3 * dist_transform.max(), 255, 0)
cv.imwrite(img_name('sure_fg'), sure_fg)

# Unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv.subtract(sure_bg, sure_fg)
cv.imwrite(img_name('unknown'), unknown)

# Marker generation
ret, markers = cv.connectedComponents(sure_fg)

# Background should be marker #0, so increment others then assign background
markers = markers + 1
markers[unknown==255] = 0

# Apply watershed and mark boundary as fuchsia
markers = cv.watershed(img, markers)
img[markers == -1] = [255, 0, 255]
cv.imwrite(img_name('out'), img);
