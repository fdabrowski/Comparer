import os

import cv2

TRAFFIC = 'traffic'
NIGHT_STREET = 'night_street'
DARK_TRAFFIC = 'dark_traffic'
LIGHT_TRAFFIC = 'light_traffic'
BLUR_TRAFFIC = 'blur_traffic'
VIDEO_NAME = BLUR_TRAFFIC
VIDEO_DIR = '/Users/filipdabrowski/Documents/video/' + VIDEO_NAME
SAVE_DIR = 'ground_truth_frames/' + VIDEO_NAME + '/frames'


def saveImage(imgcv, index):
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
    saveImage(frame, frame_count)
    frame_count += 1
