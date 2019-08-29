import argparse
import os
import cv2
import natsort
from modificator_type import ModificatorType


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("project_name", help="Set project name", type=str)
    parser.add_argument("modificator", help="Set modificator if needed. Possible modificators: [dark, light, blur]",
                        type=str)
    args = parser.parse_args()
    return args


def create_modified_video(alpha, beta):
    for image in sortedGtImages:
        img = cv2.imread(os.path.join(image_folder, image))
        img_modified = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
        video.write(img_modified)


def create_blur_video():
    for image in sortedGtImages:
        img = cv2.imread(os.path.join(image_folder, image))
        blur = cv2.blur(img, (20, 20))
        video.write(blur)


def create_dir_if_not_exists():
    if not os.path.exists(video_dir):
        os.makedirs(video_dir)


if __name__ == "__main__":
    args = parse_arguments()
    project_name = args.__dict__['project_name']
    modificator = ModificatorType[args.__dict__['modificator']]
    video_name = modificator.value + '_' + project_name
    image_folder = 'ground_truth_frames/' + project_name + '/' + project_name + '/frames'
    video_dir = '/Users/filipdabrowski/Documents/video/'
    video_path = video_dir + video_name + '.avi'
    create_dir_if_not_exists()
    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    sortedGtImages = natsort.natsorted(images)
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'DIVX'), 23, (width, height))

    if modificator == ModificatorType.dark:
        create_modified_video(0.1, 0.5)
    elif modificator == ModificatorType.light:
        create_modified_video(1, 120)
    elif modificator == ModificatorType.blur:
        create_blur_video()

    cv2.destroyAllWindows()
    video.release()
