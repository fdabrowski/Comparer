import argparse
import copy
import os
from os import listdir
from os.path import isfile, join

import cv2
import natsort

from graph_creator import get_recall_data
from src.IoUProvider import IoUProvider
from src.PairBox import PairBox
from src.ResultSaver import ResultSaver
from src.StatisticsProvider import StatisticsProvider
from src.file_readers.GroundTruthReader import GroundTruthReader
from src.file_readers.JsonReader import JsonReader
from src.utils.FinalStatistics import avarage_statistics, save_final_statistics
from src.utils.boxColors import BoxColors
from src.utils.boxDrawer import draw_predicted_objects, show_confidence

def process_yolo(index, imgcv, imgCopy):
    yolo_reader = JsonReader(project_name, video_name, sorted_yolo_file_list[index], 'yolo')
    yolo_bounding_boxes = yolo_reader.getBoundingBoxes()
    time = yolo_reader.getTime()
    yolo_bounding_boxes = list(filter(lambda x: x.object_class in available_classes, yolo_bounding_boxes))
    draw_predicted_objects(yolo_bounding_boxes, imgcv, BoxColors.CAR_COLOR, 2)
    draw_predicted_objects(yolo_bounding_boxes, imgCopy, BoxColors.CAR_COLOR, 2)
    show_confidence(yolo_bounding_boxes, imgcv, BoxColors.CAR_COLOR)
    show_confidence(yolo_bounding_boxes, imgCopy, BoxColors.CAR_COLOR)
    save_singular_image(imgCopy, index, 'yolo')
    return yolo_bounding_boxes, time


def process_ssd(index, imgcv, imgCopy):
    ssd_reader = JsonReader(project_name, video_name, sorted_ssd_file_list[index], 'ssd')
    ssd_bounding_box = ssd_reader.getBoundingBoxes()
    time = ssd_reader.getTime()
    ssd_bounding_box = list(filter(lambda x: x.object_class in available_classes, ssd_bounding_box))
    draw_predicted_objects(ssd_bounding_box, imgcv, BoxColors.SSD_COLOR, 2)
    draw_predicted_objects(ssd_bounding_box, imgCopy, BoxColors.SSD_COLOR, 2)
    show_confidence(ssd_bounding_box, imgcv, BoxColors.SSD_COLOR)
    show_confidence(ssd_bounding_box, imgCopy, BoxColors.SSD_COLOR)
    save_singular_image(imgCopy, index, 'ssd')
    return ssd_bounding_box, time


def save_image(imgcv, index):
    cv2.imwrite(OUT + '/' + str(index) + '_out.jpg', imgcv)


def save_singular_image(imgcv, index, algName):
    path = OUT + '/' + algName + '/frame/'
    if not os.path.exists(path):
        os.makedirs(path)
    cv2.imwrite(path + str(index) + '_out.jpg', imgcv)


def process_ground_truth(index, imgcv):
    gt_reader = GroundTruthReader(project_name, video_name, sorted_gt_file_list[index])
    gt_bounding_boxes = gt_reader.getBoundingBoxes()
    draw_predicted_objects(gt_bounding_boxes, imgcv, BoxColors.GT_COLOR, 2)
    return gt_bounding_boxes


def process_mask_rcnn(index, imgcv, imgCopy):
    rcnn_reader = JsonReader(project_name, video_name, sorted_mask_rcnn_file_list[index], 'mask_RCNN')
    rcnn_bounding_boxes = rcnn_reader.getBoundingBoxes()
    time = rcnn_reader.getTime()
    rcnn_bounding_boxes = list(filter(lambda x: x.object_class in available_classes, rcnn_bounding_boxes))
    draw_predicted_objects(rcnn_bounding_boxes, imgcv, BoxColors.RCNN_COLOR, 2)
    draw_predicted_objects(rcnn_bounding_boxes, imgCopy, BoxColors.RCNN_COLOR, 2)
    show_confidence(rcnn_bounding_boxes, imgcv, BoxColors.RCNN_COLOR)
    show_confidence(rcnn_bounding_boxes, imgCopy, BoxColors.RCNN_COLOR)
    save_singular_image(imgCopy, index, 'mask_RCNN')
    return rcnn_bounding_boxes, time


def save_final_results(yoloAllStatistics, maskRcnnAllStatistics, ssdAllStatistics):
    yolo_final_statistics = avarage_statistics(yoloAllStatistics, available_classes)
    mask_rcnn_final_statistics = avarage_statistics(maskRcnnAllStatistics, available_classes)
    ssd_final_statistics = avarage_statistics(ssdAllStatistics, available_classes)
    save_final_statistics(FINAL_STATISTICS, yolo_final_statistics)
    save_final_statistics(FINAL_STATISTICS, mask_rcnn_final_statistics)
    save_final_statistics(FINAL_STATISTICS, ssd_final_statistics)


def save_single_result(dir, pairs, iouResult, fileName, statistics):
    resultSaver = ResultSaver(OUT + dir)
    resultSaver.save_result(pairs, iouResult, fileName, statistics)


def create_pairs(gt_bounding_boxes, predict_bounding_boxes):
    yoloPairBox = PairBox()
    return yoloPairBox.find_predicted(gt_bounding_boxes, predict_bounding_boxes)

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("project_name", help="Set project name.", type=str)
    parser.add_argument("video_name", help="Set video name.", type=str)
    parser.add_argument("--available_classes", nargs="*", help="Put classes of objects which are possible to be detected.", type=str)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parseArguments()
    project_name = args.__dict__['project_name']
    video_name = args.__dict__['video_name']
    available_classes = args.__dict__['available_classes']

    GT_FRAMES = 'ground_truth_frames/' + project_name + '/' + video_name + '/frames'
    GT_BOXES = 'ground_truth_frames/' + project_name + '/' + video_name + '/boxes'
    MASK_RCNN_BOXES = 'mask_RCNN/' + project_name + '/' + video_name + '/boxes'
    SSD_BOXES = 'ssd/' + project_name + '/' + video_name + '/boxes'
    YOLO_BOXES = 'yolo/' + project_name + '/' + video_name + '/boxes'
    OUT = 'out/' + project_name + '/' + video_name
    FINAL_STATISTICS = OUT + '/statistics'

    all_gt_files = [f for f in listdir(GT_BOXES) if isfile(join(GT_BOXES, f))]
    all_gt_images = [f for f in listdir(GT_FRAMES) if isfile(join(GT_FRAMES, f))]
    all_yolo_files = [f for f in listdir(YOLO_BOXES) if isfile(join(YOLO_BOXES, f))]
    all_mask_rcnn_files = [f for f in listdir(MASK_RCNN_BOXES) if isfile(join(MASK_RCNN_BOXES, f))]
    all_ssd_files = [f for f in listdir(SSD_BOXES) if isfile(join(SSD_BOXES, f))]

    sorted_gt_file_list = natsort.natsorted(all_gt_files)
    sorted_gt_images = natsort.natsorted(all_gt_images)

    sorted_yolo_file_list = natsort.natsorted(all_yolo_files)
    sorted_mask_rcnn_file_list = natsort.natsorted(all_mask_rcnn_files)
    sorted_ssd_file_list = natsort.natsorted(all_ssd_files)

    all_bounding_box = []

    if not os.path.exists(OUT):
        os.makedirs(OUT)

    yolo_all_statistics = []
    mask_rcnn_all_statistics = []
    ssd_all_statistics = []

    for index in range(0, len(sorted_gt_file_list)):
        fileName = sorted_gt_images[index]
        imgcv = cv2.imread(GT_FRAMES + '/' + fileName)

        imgcv_yolo = copy.copy(imgcv)
        imgcv_rcnn = copy.copy(imgcv)
        imgcv_ssd = copy.copy(imgcv)

        gt_bounding_boxes = process_ground_truth(index, imgcv)
        yolo_bounding_boxes, yoloTime = process_yolo(index, imgcv, imgcv_yolo)
        rcnn_bounding_boxes, rcnnTime = process_mask_rcnn(index, imgcv, imgcv_rcnn)
        ssd_bounding_boxes, ssdTime = process_ssd(index, imgcv, imgcv_ssd)

        yolo_pairs = create_pairs(gt_bounding_boxes, yolo_bounding_boxes)
        ssd_pairs = create_pairs(gt_bounding_boxes, ssd_bounding_boxes)
        mask_rcnn_pairs = create_pairs(gt_bounding_boxes, rcnn_bounding_boxes)

        iou_provider = IoUProvider()
        iou_yolo_result = iou_provider.getIouResult(yolo_pairs)
        iou_mask_rcnn_result = iou_provider.getIouResult(mask_rcnn_pairs)
        iou_ssd_result = iou_provider.getIouResult(ssd_pairs)

        yolo_statistics_provider = StatisticsProvider('yolo', gt_bounding_boxes, yolo_bounding_boxes, yolo_pairs,
                                                    iou_yolo_result, yoloTime)
        yolo_statistics = yolo_statistics_provider.returnStatistics()
        yolo_all_statistics.append(yolo_statistics)

        mask_rcnn_statistics_provider = StatisticsProvider('maskRCNN', gt_bounding_boxes, rcnn_bounding_boxes, mask_rcnn_pairs,
                                                        iou_mask_rcnn_result, rcnnTime)
        mask_rcnn_statistics = mask_rcnn_statistics_provider.returnStatistics()
        mask_rcnn_all_statistics.append(mask_rcnn_statistics)

        ssd_statistics_provider = StatisticsProvider('ssd', gt_bounding_boxes, ssd_bounding_boxes, ssd_pairs,
                                                   iou_ssd_result, ssdTime)
        ssd_statistics = ssd_statistics_provider.returnStatistics()
        ssd_all_statistics.append(ssd_statistics)

        save_single_result('/yolo/iou', yolo_pairs, iou_yolo_result, fileName, yolo_statistics)
        save_single_result('/mask_RCNN/iou', mask_rcnn_pairs, iou_mask_rcnn_result, fileName, mask_rcnn_statistics)
        save_single_result('/ssd/iou', ssd_pairs, iou_ssd_result, fileName, ssd_statistics)

        save_image(imgcv, index)

    get_recall_data(yolo_all_statistics, available_classes, 'YOLO')
    get_recall_data(ssd_all_statistics, available_classes, 'SSD')
    get_recall_data(mask_rcnn_all_statistics, available_classes, 'Faster RCNN')
    save_final_results(yolo_all_statistics, mask_rcnn_all_statistics, ssd_all_statistics)

