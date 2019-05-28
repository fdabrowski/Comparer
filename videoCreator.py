import cv2
import os

import natsort
# image_folder = 'ground_truth_frames/night_street/boxes'
image_folder = 'ground_truth_frames/dark_traffic/boxes'
# image_folder = 'out/night_street'
VIDEO_DIR = '/Users/filipdabrowski/Documents/video/'
video_name = VIDEO_DIR + 'dark_traffic.avi'

alpha = 0.1 # Simple contrast control
beta = 20 # Simple brightness control

images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, 29.9, (width,height))
sortedGtImages = natsort.natsorted(images)
for image in sortedGtImages:
    img = cv2.imread(os.path.join(image_folder, image))
    imgDark = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
    video.write(imgDark)

cv2.destroyAllWindows()
video.release()