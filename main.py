import copy
import sys
from os import listdir
from os.path import isfile, join
import cv2
import os
import natsort
from src.utils.FinalStatistics import avarageStatistics, saveFinalStatistics
from src.IoUProvider import IoUProvider
from src.PairBox import PairBox
from src.ResultSaver import ResultSaver
from src.StatisticsProvider import StatisticsProvider
from src.file_readers.GroundTruthReader import GroundTruthReader
from src.file_readers.JsonReader import JsonReader
from src.utils.boxColors import BoxColors
from src.utils.boxDrawer import drawPredictedObjects, showConfidence

TRAFFIC = 'traffic'
NIGHT_STREET = 'night_street'
DARK_TRAFFIC = 'dark_traffic'
LIGHT_TRAFFIC = 'light_traffic'
BLUR_TRAFFIC = 'blur_traffic'
DARK = 'dark_'
LIGHT = 'light_'
BLUR = 'blur_'
PROJECT_NAME = LIGHT + NIGHT_STREET

GT_FRAMES = '../ground_truth_frames/' + PROJECT_NAME + '/frames'
GT_BOXES = '../ground_truth_frames/' + PROJECT_NAME + '/boxes'
MASK_RCNN_BOXES = '../mask_RCNN/' + PROJECT_NAME + '/boxes'
SSD_BOXES = '../ssd/' + PROJECT_NAME + '/boxes'
YOLO_BOXES = '../yolo/' + PROJECT_NAME + '/boxes'
OUT = '../out/' + PROJECT_NAME
FINAL_STATISTICS = OUT + '/statistics'

allGtFiles = [f for f in listdir(GT_BOXES) if isfile(join(GT_BOXES, f))]
allGtImages = [f for f in listdir(GT_FRAMES) if isfile(join(GT_FRAMES, f))]
allYoloFIles = [f for f in listdir(YOLO_BOXES) if isfile(join(YOLO_BOXES, f))]
allMaskRCNNFIles = [f for f in listdir(MASK_RCNN_BOXES) if isfile(join(MASK_RCNN_BOXES, f))]
allSSDFiles = [f for f in listdir(SSD_BOXES) if isfile(join(SSD_BOXES, f))]

sortedGtFileList = natsort.natsorted(allGtFiles)
sortedGtImages = natsort.natsorted(allGtImages)

sortedYoloFileList = natsort.natsorted(allYoloFIles)
sortedMaskRCNNFileList = natsort.natsorted(allMaskRCNNFIles)
sortedSSDFileList = natsort.natsorted(allSSDFiles)

allBoundingBox = []

if not os.path.exists(OUT):
    os.makedirs(OUT)

def run() -> None:
    yoloAllStatistics = []
    maskRcnnAllStatistics = []
    ssdAllStatistics = []

    for index in range(0, len(sortedGtFileList)):
        fileName = sortedGtImages[index]
        imgcv = cv2.imread(GT_FRAMES + '/' + fileName)

        imgcvYolo = copy.copy(imgcv)
        imgcvRcnn = copy.copy(imgcv)
        imgcvSSD = copy.copy(imgcv)

        gtBoundingBoxes = processGroundTruth(index, imgcv)
        yoloBoundingBoxes, yoloTime = processYolo(index, imgcv, imgcvYolo)
        rcnnBoundingBoxes, rcnnTime = processMaskRcnn(index, imgcv, imgcvRcnn)
        ssdBoundingBoxes, ssdTime = processSSD(index, imgcv, imgcvSSD)

        yoloPairs = createPairs(gtBoundingBoxes, yoloBoundingBoxes)
        maskRCNNPairs = createPairs(gtBoundingBoxes, rcnnBoundingBoxes)
        ssdPairs = createPairs(gtBoundingBoxes, ssdBoundingBoxes)

        iouProvider = IoUProvider()
        iouYoloResult = iouProvider.getIouResult(yoloPairs)
        iouMaskRCNNResult = iouProvider.getIouResult(maskRCNNPairs)
        iouSSDResult = iouProvider.getIouResult(ssdPairs)

        yoloStatisticsProvider = StatisticsProvider('yolo', gtBoundingBoxes, yoloBoundingBoxes, yoloPairs,
                                                    iouYoloResult, yoloTime)
        yoloAllStatistics.append(yoloStatisticsProvider.returnStatistics())

        maskRcnnStatisticsProvider = StatisticsProvider('maskRCNN', gtBoundingBoxes, rcnnBoundingBoxes, maskRCNNPairs,
                                                        iouMaskRCNNResult, rcnnTime)
        maskRcnnAllStatistics.append(maskRcnnStatisticsProvider.returnStatistics())

        ssdStatisticsProvider = StatisticsProvider('ssd', gtBoundingBoxes, ssdBoundingBoxes, ssdPairs,
                                                   iouSSDResult, ssdTime)
        ssdAllStatistics.append(ssdStatisticsProvider.returnStatistics())

        saveSingleResult('/yolo/iou', yoloPairs, iouYoloResult, fileName)
        saveSingleResult('/mask_RCNN/iou', maskRCNNPairs, iouMaskRCNNResult, fileName)
        saveSingleResult('/ssd/iou', ssdPairs, iouSSDResult, fileName)
        saveImage(imgcv, index)

    saveFinalResults(yoloAllStatistics, maskRcnnAllStatistics, ssdAllStatistics)


def processYolo(index, imgcv, imgCopy):
    yoloReader = JsonReader(PROJECT_NAME, sortedYoloFileList[index], 'yolo')
    yoloBoundingBoxes = yoloReader.getBoundingBoxes()
    time = yoloReader.getTime()
    yoloBoundingBoxes = list(filter(lambda x: x.objectClass == 'person', yoloBoundingBoxes))
    drawPredictedObjects(yoloBoundingBoxes, imgcv, BoxColors.CAR_COLOR, 2)
    drawPredictedObjects(yoloBoundingBoxes, imgCopy, BoxColors.CAR_COLOR, 2)
    showConfidence(yoloBoundingBoxes, imgcv, BoxColors.CAR_COLOR)
    showConfidence(yoloBoundingBoxes, imgCopy, BoxColors.CAR_COLOR)
    saveSingularImage(imgCopy, index, 'yolo')
    return yoloBoundingBoxes, time


def processSSD(index, imgcv, imgCopy):
    ssdReader = JsonReader(PROJECT_NAME, sortedSSDFileList[index], 'ssd')
    ssdBoundingBox = ssdReader.getBoundingBoxes()
    time = ssdReader.getTime()
    ssdBoundingBox = list(filter(lambda x: x.objectClass == 'person', ssdBoundingBox))
    drawPredictedObjects(ssdBoundingBox, imgcv, BoxColors.SSD_COLOR, 2)
    drawPredictedObjects(ssdBoundingBox, imgCopy, BoxColors.SSD_COLOR, 2)
    showConfidence(ssdBoundingBox, imgcv, BoxColors.SSD_COLOR)
    showConfidence(ssdBoundingBox, imgCopy, BoxColors.SSD_COLOR)
    saveSingularImage(imgCopy, index, 'ssd')
    return ssdBoundingBox, time


def saveImage(imgcv, index):
    cv2.imwrite(OUT + '/' + str(index) + '_out.jpg', imgcv)


def saveSingularImage(imgcv, index, algName):
    path = OUT + '/' + algName + '/frame/'
    if not os.path.exists(path):
        os.makedirs(path)
    cv2.imwrite(path + str(index) + '_out.jpg', imgcv)


def processGroundTruth(index, imgcv):
    gtReader = GroundTruthReader(PROJECT_NAME, sortedGtFileList[index])
    gtBoundingBoxes = gtReader.getBoundingBoxes()
    drawPredictedObjects(gtBoundingBoxes, imgcv, BoxColors.GT_COLOR, 2)
    return gtBoundingBoxes


def processMaskRcnn(index, imgcv, imgCopy):
    rcnnReader = JsonReader(PROJECT_NAME, sortedMaskRCNNFileList[index], 'mask_RCNN')
    rcnnBoundingBoxes = rcnnReader.getBoundingBoxes()
    time = rcnnReader.getTime()
    rcnnBoundingBoxes = list(filter(lambda x: x.objectClass == 'person', rcnnBoundingBoxes))
    drawPredictedObjects(rcnnBoundingBoxes, imgcv, BoxColors.RCNN_COLOR, 2)
    drawPredictedObjects(rcnnBoundingBoxes, imgCopy, BoxColors.RCNN_COLOR, 2)
    showConfidence(rcnnBoundingBoxes, imgcv, BoxColors.RCNN_COLOR)
    showConfidence(rcnnBoundingBoxes, imgCopy, BoxColors.RCNN_COLOR)
    saveSingularImage(imgCopy, index, 'mask_RCNN')
    return rcnnBoundingBoxes, time


def saveFinalResults(yoloAllStatistics, maskRcnnAllStatistics, ssdAllStatistics):
    yoloFinalStatistics = avarageStatistics(yoloAllStatistics)
    maskRcnnFinalStatistics = avarageStatistics(maskRcnnAllStatistics)
    ssdFinalStatistics = avarageStatistics(ssdAllStatistics)
    saveFinalStatistics(FINAL_STATISTICS, yoloFinalStatistics)
    saveFinalStatistics(FINAL_STATISTICS, maskRcnnFinalStatistics)
    saveFinalStatistics(FINAL_STATISTICS, ssdFinalStatistics)


def saveSingleResult(dir, pairs, iouResult, fileName):
    resultSaver = ResultSaver(OUT + dir)
    resultSaver.saveResult(pairs, iouResult, fileName)


def createPairs(gtBoundingBoxes, predictBoundingBoxes):
    yoloPairBox = PairBox()
    return yoloPairBox.findPredicted(gtBoundingBoxes, predictBoundingBoxes)


run()
