import os

import cv2
import natsort

# image_folder = 'ground_truth_frames/traffic/frames'
# image_folder = 'out/night_street'
# image_folder = 'out/night_street/'
# VIDEO_DIR = '/Users/filipdabrowski/Documents/video/'
DARK = 'dark_'
LIGHT = 'light_'
BLUR = 'blur_'
ANIMALS = 'animals'
PERSON = 'person'
GLASS = 'glass'
FRUITS = 'fruits'
BIKE = 'bike'
PROJECT_NAME = BIKE
VIDEO_NAME = LIGHT + BIKE
image_folder = 'ground_truth_frames/' + PROJECT_NAME + '/frames'
VIDEO_DIR = '/Users/filipdabrowski/Documents/video/out/' + PROJECT_NAME + '/' + VIDEO_NAME + '/'

VIDEO_PATH = VIDEO_DIR + VIDEO_NAME + '.avi'

if not os.path.exists(VIDEO_DIR):
    os.makedirs(VIDEO_DIR)

# light
alpha = 2 # Simple contrast control
beta = 150 # Simple brightness control

# # # dark
# alpha = 0.1# Simple contrast control
# beta = 5 # Simple brightness control

# VIDEO_HEIGHT = 800
# VIDEO_WIDTH = 1024

images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

# height, width = (VIDEO_HEIGHT, VIDEO_WIDTH)

video = cv2.VideoWriter(VIDEO_PATH, cv2.VideoWriter_fourcc(*'DIVX'), 23, (width, height))
sortedGtImages = natsort.natsorted(images)
for image in sortedGtImages:
    img = cv2.imread(os.path.join(image_folder, image))
    # img = cv2.resize(img, (VIDEO_WIDTH, VIDEO_HEIGHT))

    img_modified = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    # blur = cv2.blur(img, (20, 20))
    video.write(img_modified)

cv2.destroyAllWindows()
video.release()
