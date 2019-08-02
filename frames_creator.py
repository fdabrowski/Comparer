import argparse
import os
import cv2

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("project_name", help="Set project name", type=str)
    parser.add_argument("video_name", help="Set project name", type=str)
    parser.add_argument("extension", help="Set file extension", type=str)
    args = parser.parse_args()
    return args

def save_image(imgcv, index):
    cv2.imwrite(save_dir + '/frame' + str(index) + '.jpg', imgcv)

def create_if_dir_not_exsists():
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

if __name__ == "__main__":
    args = parse_arguments()
    project_name = args.__dict__['project_name']
    video_name = args.__dict__['video_name']
    extension = args.__dict__['extension']
    video_dir = '/Users/filipdabrowski/Documents/video/' + video_name
    save_dir = 'ground_truth_frames/' + project_name + '/' + video_name + '/frames'
    create_if_dir_not_exsists()
    capture = cv2.VideoCapture(video_dir + '.' + extension)
    frame_count = 0

    while True:
        ret, frame = capture.read()
        # Bail out when the video file ends
        if not ret:
            break
        # Save each frame of the video to a list
        save_image(frame, frame_count)
        frame_count += 1
