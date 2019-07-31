import argparse
import os
from label_source import LabelSource


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("video_path", help="Set video path.", type=str)
    parser.add_argument("label_source", help="Set label source.", type=str)
    args = parser.parse_args()
    return args

def create_dir_if_not_exists(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

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

def create_labels():
    if label_source == LabelSource.cvat:
        cvat_script = "python3 xml_converter.xml.py " + project_name
        os.system(cvat_script)
        print(cvat_script)

def copy_labels_to_modified():
    gt_path = 'ground_truth_frames/' + project_name + '/' + project_name + '/boxes'
    dark_path = 'ground_truth_frames/' + project_name + '/dark_' + project_name
    light_path = 'ground_truth_frames/' + project_name + '/light_' + project_name
    blur_path = 'ground_truth_frames/' + project_name + '/blur_' + project_name

    create_dir_if_not_exists(dark_path)
    create_dir_if_not_exists(light_path)
    create_dir_if_not_exists(blur_path)

    copy_dark_script = 'cp -R ' + gt_path + ' ' + dark_path
    copy_light_script = 'cp -R ' + gt_path + ' ' + light_path
    copy_blur_script = 'cp -R ' + gt_path + ' ' + blur_path

    print(copy_dark_script)
    os.system(copy_dark_script)
    print(copy_light_script)
    os.system(copy_light_script)
    print(copy_blur_script)
    os.system(copy_blur_script)

if __name__ == "__main__":
    args = parseArguments()
    video_name = args.__dict__['video_path']
    label_source = LabelSource[args.__dict__['label_source']]
    project_name, format = video_name.split('.')

    print('=========================== WHOOOOOLE PROCESS STARTED ===========================')
    print('====== 1. Prepare ground truth images ======')
    # Create main ground truth images
    create_main_gt_images()
    # Create modified videos
    create_modified_videos()
    # Create modified ground truth images
    create_modified_gt_images()
    print('====== 2. Prepare labels ======')
    create_labels()
    copy_labels_to_modified()
    print('====== 3. Run YOLO ======')

    print('====== 4. Run SSD ======')

    print('====== 5. Run Faster R-CNN ======')


    print(video_name)
    print(label_source)
    print(project_name)

