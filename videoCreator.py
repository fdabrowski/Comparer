import cv2
import os

import natsort
image_folder = 'ground_truth_frames/night_street/boxes'
# image_folder = 'out/night_street'
video_name = 'night_street.avi'

images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, 30, (width,height))
sortedGtImages = natsort.natsorted(images)
for image in sortedGtImages:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()