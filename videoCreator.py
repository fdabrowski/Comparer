import numpy as np

import cv2
import os

import natsort
image_folder = 'ground_truth_frames/night_street/frames'
# image_folder = 'ground_truth_frames/traffic/frames'
# image_folder = 'out/night_street'
# image_folder = 'out/night_street/'
# VIDEO_DIR = '/Users/filipdabrowski/Documents/video/'
PROJECT_NAME = 'night_street'
VIDEO_NAME = 'blur_night_street'
VIDEO_DIR = '/Users/filipdabrowski/Documents/video/out/' + PROJECT_NAME + '/' + VIDEO_NAME + '/'

VIDEO_PATH = VIDEO_DIR + VIDEO_NAME +'.avi'

if not os.path.exists(VIDEO_DIR):
    os.makedirs(VIDEO_DIR)

# light
alpha = 1 # Simple contrast control
beta = 100# Simple brightness control

# # dark
# alpha = 0.1 # Simple contrast control
# beta = 20 # Simple brightness control

images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(VIDEO_PATH, cv2.VideoWriter_fourcc(*'DIVX'), 29.9, (width,height))
sortedGtImages = natsort.natsorted(images)
for image in sortedGtImages:
    img = cv2.imread(os.path.join(image_folder, image))
    # imgModified = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    # blur = cv2.blur(img, (15, 15))
    video.write(img)

cv2.destroyAllWindows()
video.release()