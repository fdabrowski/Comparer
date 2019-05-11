from os import listdir
from os.path import isfile, join
import cv2
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

GT_FRAMES = '../ground_truth_frames/traffic/frames'
GT_BOXES = '../ground_truth_frames/traffic/boxes'
MASK_RCNN_BOXES = '../mask_RCNN/traffic/boxes'
MASK_RCNN_FRAMES = '../mask_RCNN/traffic/frames'
YOLO_FRAMES = '../yolo/traffic/frames'
YOLO_BOXES = '../yolo/traffic/boxes'
OUT = '../out/traffic'
FINAL_STATISTICS = OUT + '/statistics'

allGtFiles = [f for f in listdir(GT_BOXES) if isfile(join(GT_BOXES, f))]
allGtImages = [f for f in listdir(GT_FRAMES) if isfile(join(GT_FRAMES, f))]
allYoloFIles = [f for f in listdir(YOLO_BOXES) if isfile(join(YOLO_BOXES, f))]
allMaskRCNNFIles = [f for f in listdir(MASK_RCNN_BOXES) if isfile(join(MASK_RCNN_BOXES, f))]

sortedGtFileList = natsort.natsorted(allGtFiles)
sortedGtImages = natsort.natsorted(allGtImages)
sortedYoloFileList = natsort.natsorted(allYoloFIles)
sortedMaskRCNNFileList = natsort.natsorted(allMaskRCNNFIles)

allBoundingBox = []


def run() -> None:
    yoloAllStatistics = []
    maskRcnnAllStatistics = []

    for index in range(0, len(sortedGtFileList)):
        fileName = sortedGtImages[index]
        imgcv = cv2.imread(GT_FRAMES + '/' + fileName)

        gtBoundingBoxes = processGroundTruth(index, imgcv)
        yoloBoundingBoxes = processYolo(index, imgcv)
        rcnnBoundingBoxes = processMaskRcnn(index, imgcv)

        yoloPairs = createPairs(gtBoundingBoxes, yoloBoundingBoxes)
        maskRCNNPairs = createPairs(gtBoundingBoxes, rcnnBoundingBoxes)

        iouProvider = IoUProvider()
        iouYoloResult = iouProvider.getIouResult(yoloPairs)
        iouMaskRCNNResult = iouProvider.getIouResult(maskRCNNPairs)

        # markPairedBoxes(imgcv, pairs)

        yoloStatisticsProvider = StatisticsProvider('yolo', gtBoundingBoxes, yoloBoundingBoxes, yoloPairs,
                                                    iouYoloResult)
        yoloStatistics = yoloStatisticsProvider.returnStatistics()
        yoloAllStatistics.append(yoloStatistics)

        maskRcnnStatisticsProvider = StatisticsProvider('maskRCNN', gtBoundingBoxes, rcnnBoundingBoxes, maskRCNNPairs,
                                                        iouMaskRCNNResult)
        maskRcnnStatistics = maskRcnnStatisticsProvider.returnStatistics()
        maskRcnnAllStatistics.append(maskRcnnStatistics)

        saveSingleResult('/yolo/iou', yoloPairs, iouYoloResult, fileName)
        saveSingleResult('/mask_RCNN/iou', maskRCNNPairs, iouMaskRCNNResult, fileName)
        saveImage(imgcv, index)

    saveFinalResults(yoloAllStatistics, maskRcnnAllStatistics)

def processYolo(index, imgcv):
    yoloReader = JsonReader('traffic', sortedYoloFileList[index], 'yolo')
    yoloBoundingBoxes = yoloReader.getBoundingBoxes()
    drawPredictedObjects(yoloBoundingBoxes, imgcv, BoxColors.CAR_COLOR, 2)
    showConfidence(yoloBoundingBoxes, imgcv, BoxColors.CAR_COLOR)
    return yoloBoundingBoxes

def saveImage(imgcv, index):
    cv2.imwrite(OUT + '/' + str(index) + '_out.jpg', imgcv)

def processGroundTruth(index, imgcv):
    gtReader = GroundTruthReader('traffic', sortedGtFileList[index])
    gtBoundingBoxes = gtReader.getBoundingBoxes()
    drawPredictedObjects(gtBoundingBoxes, imgcv, BoxColors.GT_COLOR, 2)
    return gtBoundingBoxes

def processMaskRcnn(index, imgcv):
    rcnnReader = JsonReader('traffic', sortedMaskRCNNFileList[index], 'mask_RCNN')
    rcnnBoundingBoxes = rcnnReader.getBoundingBoxes()
    drawPredictedObjects(rcnnBoundingBoxes, imgcv, BoxColors.RCNN_COLOR, 2)
    showConfidence(rcnnBoundingBoxes, imgcv, BoxColors.RCNN_COLOR)
    return rcnnBoundingBoxes

def saveFinalResults(yoloAllStatistics, maskRcnnAllStatistics):
    yoloFinalStatistics = avarageStatistics(yoloAllStatistics)
    maskRcnnFinalStatistics = avarageStatistics(maskRcnnAllStatistics)
    saveFinalStatistics(FINAL_STATISTICS, yoloFinalStatistics)
    saveFinalStatistics(FINAL_STATISTICS, maskRcnnFinalStatistics)

def saveSingleResult(dir, pairs, iouResult, fileName):
    resultSaver = ResultSaver(OUT + dir)
    resultSaver.saveResult(pairs, iouResult, fileName)

def createPairs(gtBoundingBoxes, predictBoundingBoxes):
    yoloPairBox = PairBox()
    return yoloPairBox.findPredicted(gtBoundingBoxes, predictBoundingBoxes)


run()
