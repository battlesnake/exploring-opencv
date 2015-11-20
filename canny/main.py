#!/usr/bin/python3

import numpy as np
import cv2 as cv

img_base_name = 'sample'
img_index = 0

width = 1024
height = 768

def img_name(suffix = None, suffix2 = None):
    global img_index
    name = img_base_name
    if suffix:
        img_index = img_index + 1
        name = name + '-' + str(img_index) + '-' + suffix
        if suffix2:
            name = name + '-' + suffix2
    return name + '.jpg'

# Load image and rescale
original = cv.imread(img_name())
img = cv.resize(original, (width, height))
cv.imwrite(img_name('scale'), img)

# Get normalized grayscale image for thresholding
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
gray = clahe.apply(gray)
cv.imwrite(img_name('gray'), gray)

# Filtering
filtered = cv.bilateralFilter(gray, 5, 100, 100)
cv.imwrite(img_name('filtered'), filtered)

def render_contours(rejection, color):
    lower = 40 * rejection
    upper = 80 * rejection
    # Canny
    canny = cv.Canny(filtered, lower, upper)
    # Segmentation
    null, contours, hierarchy = cv.findContours(canny, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    # Render
    vis = np.zeros((height, width, 3), np.uint8)
    cv.drawContours(vis, contours, -1, color, 1)
    cv.imwrite(img_name('contour'), vis)
    return vis

layer1 = render_contours(1, (0,0,255))
layer2 = render_contours(2, (0,255,0))
layer3 = render_contours(3, (255,0,0))

# Since there's no fucking overload for the *= /= operators
img = cv.addWeighted(img, 0.5, img, 0, 0)
contour = cv.add(img, cv.add(layer1, cv.add(layer2, layer3)))
cv.imwrite(img_name('contours'), contour)
