import glob

import numpy as np

import cv2
import os

import natsort

# image_folder = 'ground_truth_frames/traffic/frames'
# image_folder = 'out/night_street'
# image_folder = 'out/night_street/'
# VIDEO_DIR = '/Users/filipdabrowski/Documents/video/'
DARK = 'dark_'
LIGHT = 'light_'
BLUR = 'blur_'
ANIMALS = 'animals'
PROJECT_NAME = ANIMALS
VIDEO_NAME = LIGHT + ANIMALS
image_folder = 'ground_truth_frames/' + PROJECT_NAME + '/frames'
VIDEO_DIR = '/Users/filipdabrowski/Documents/video/out/' + PROJECT_NAME + '/' + VIDEO_NAME + '/'

VIDEO_PATH = VIDEO_DIR + VIDEO_NAME + '.avi'

if not os.path.exists(VIDEO_DIR):
    os.makedirs(VIDEO_DIR)

# light
# alpha = 1  # Simple contrast control
# beta = 100  # Simple brightness control

# # dark
# alpha = 0.1 # Simple contrast control
# beta = 20 # Simple brightness control

VIDEO_HEIGHT = 1024
VIDEO_WIDTH = 800

images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
# height, width, layers = frame.shape

height, width = (VIDEO_HEIGHT, VIDEO_WIDTH)

video = cv2.VideoWriter(VIDEO_PATH, cv2.VideoWriter_fourcc(*'DIVX'), 1, (height, width))
sortedGtImages = natsort.natsorted(images)
for image in sortedGtImages:
    img = cv2.imread(os.path.join(image_folder, image))
    img = cv2.resize(img, (VIDEO_HEIGHT, VIDEO_WIDTH))

    # imgModified = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    # blur = cv2.blur(img, (15, 15))
    video.write(img)

# cv2.destroyAllWindows()
video.release()
