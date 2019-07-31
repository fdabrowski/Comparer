import argparse
import os
from label_source import LabelSource


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("video_path", help="Set video path.", type=str)
    parser.add_argument("label_source", help="Set label source.", type=str)
    args = parser.parse_args()
    return args

def create_modified_videos():
    dark_script = "python3 video_creator.py " + project_name + " dark"
    light_script = "python3 video_creator.py " + project_name + " light"
    blur_script = "python3 video_creator.py " + project_name + " blur"
    os.system(dark_script)
    print(dark_script)
    os.system(light_script)
    print(light_script)
    os.system(blur_script)
    print(blur_script)

def create_main_gt_images():
    gt_script = "python3 frames_creator.py " + project_name + " " + project_name + " " + format
    os.system(gt_script)
    print(gt_script)

def create_modified_gt_images():
    dark_script = "python3 frames_creator.py " + project_name + " dark_" + project_name + " avi"
    light_script = "python3 frames_creator.py " + project_name + " light_" + project_name + " avi"
    blur_script = "python3 frames_creator.py " + project_name + " blur_" + project_name + " avi"

    os.system(dark_script)
    print(dark_script)
    os.system(light_script)
    print(light_script)
    os.system(blur_script)
    print(blur_script)

if __name__ == "__main__":
    args = parseArguments()
    video_name = args.__dict__['video_path']
    label_source = LabelSource[args.__dict__['label_source']]
    project_name, format = video_name.split('.')

    print('=========================== WHOOOOOLE PROCESS STARTED ===========================')
    # Create main ground truth images
    create_main_gt_images()
    # Create modified videos
    create_modified_videos()
    # Create modified ground truth images
    create_modified_gt_images()


    print(video_name)
    print(label_source)
    print(project_name)

