import os

import cv2

TRAFFIC = 'traffic'
ANIMALS = 'animals'
NIGHT_STREET = 'night_street'
PERSON = 'person'
GLASS = 'glass'
DARK = 'dark_'
LIGHT = 'light_'
BLUR = 'blur_'
VIDEO_NAME = GLASS
VIDEO_DIR = '/Users/filipdabrowski/Documents/video/' + VIDEO_NAME
SAVE_DIR = 'ground_truth_frames/' + VIDEO_NAME + '/frames'


def save_image(imgcv, index):
    cv2.imwrite(SAVE_DIR + '/frame' + str(index) + '.jpg', imgcv)

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

capture = cv2.VideoCapture(VIDEO_DIR + '.avi')
frame_count = 0

while True:
    ret, frame = capture.read()
    # Bail out when the video file ends
    if not ret:
        break
    # Save each frame of the video to a list
    save_image(frame, frame_count)
    frame_count += 1
