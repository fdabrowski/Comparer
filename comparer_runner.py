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


def run_yolo(project_name, extension):
    yolo_script = 'cd /Users/filipdabrowski/Documents/git/darkflow/ && ' \
                  'python3 flow --model cfg/yolo.cfg --load bin/yolo.weights ' \
                  '--demo /Users/filipdabrowski/Documents/video/' + project_name + '.' + extension + \
                  ' --saveVideo --projectName ' + project_name
    print(yolo_script)
    os.system(yolo_script)

def run_ssd(project_name, extension):
    ssd_script = 'cd /Users/filipdabrowski/Documents/git/ssd_keras/ && ' \
                  'python3 sssd_coco.py ' +project_name + ' ' + extension
    print(ssd_script)
    os.system(ssd_script)

def run_faster_rcnn(project_name, extension):
    mask_rcnn_script = 'cd /Users/filipdabrowski/Documents/git/Mask_RCNN/samples/ && ' \
                  'python3 mask_rcnn.py ' +project_name + ' ' + extension
    print(mask_rcnn_script)
    os.system(mask_rcnn_script)

def run_yolo_for_all():
    print('=== 3.1 Start yolo for standard video')
    run_yolo(project_name, format)
    print('=== 3.2 Start yolo for dark video')
    run_yolo('dark_' + project_name, 'avi')
    print('=== 3.3 Start yolo for light video')
    run_yolo('light_' + project_name, 'avi')
    print('=== 3.4 Start yolo for blur video')
    run_yolo('blur_' + project_name, 'avi')

def run_mask_rcnn_for_all():
    print('=== 5.1 Start Faster R-CNN for standard video')
    run_faster_rcnn(project_name, format)
    print('=== 5.2 Start Faster R-CNN for dark video')
    run_faster_rcnn('dark_' + project_name, 'avi')
    print('=== 5.3 Start Faster R-CNN for light video')
    run_faster_rcnn('light_' + project_name, 'avi')
    print('=== 5.4 Start Faster R-CNN for blur video')
    run_faster_rcnn('blur_' + project_name, 'avi')

def run_ssd_for_all():
    print('=== 4.1 Start SSD for standard video')
    run_ssd(project_name, format)
    print('=== 4.2 Start SSD for dark video')
    run_ssd('dark_' + project_name, 'avi')
    print('=== 4.3 Start SSD for light video')
    run_ssd('light_' + project_name, 'avi')
    print('=== 4.4 Start SSD for blur video')
    run_ssd('blur_' + project_name, 'avi')


if __name__ == "__main__":
    args = parseArguments()
    video_name = args.__dict__['video_path']
    label_source = LabelSource[args.__dict__['label_source']]
    project_name, format = video_name.split('.')

    print('=========================== WHOOOOOLE PROCESS STARTED ===========================')
    print('====== 1. Prepare ground truth images ======')
    create_main_gt_images()
    create_modified_videos()
    create_modified_gt_images()

    print('====== 2. Prepare labels ======')
    create_labels()
    copy_labels_to_modified()

    print('====== 3. Run YOLO ======')
    run_yolo_for_all
    print('====== 3. End YOLO ======')

    print('====== 4. Run SSD ======')
    run_ssd_for_all
    print('====== 4. End SSD ======')

    print('====== 5. Run Faster R-CNN ======')
    run_mask_rcnn_for_all()
    print('====== 5. End Faster R-CNN ======')

    print('====== 6. Run Object Detection Comparer ======')
    # run here all staff from main.py
    print('====== 6. End Object Detection Comparer ======')


    print(video_name)
    print(label_source)
    print(project_name)
