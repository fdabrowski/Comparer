import json
from os import listdir
from os.path import isfile, join
import cv2
import natsort
from src.FinalStatistics import avarageStatistics
from src.IoUProvider import IoUProvider
from src.PairBox import PairBox
from src.ResultSaver import ResultSaver
from src.StatisticsProvider import StatisticsProvider
from src.file_readers.GroundTruthReader import GroundTruthReader
from src.file_readers.JsonReader import JsonReader
from src.model import Statistics
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

        yoloPairBox = PairBox()
        yoloPairs = yoloPairBox.findPredicted(gtBoundingBoxes, yoloBoundingBoxes)

        maskRCNNPairBox = PairBox()
        maskRCNNPairs = maskRCNNPairBox.findPredicted(gtBoundingBoxes, rcnnBoundingBoxes)

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

        yoloResultSaver = ResultSaver(OUT + '/yolo/iou')
        yoloResultSaver.saveResult(yoloPairs, iouYoloResult, fileName)

        maskRCNNResultSaver = ResultSaver(OUT + '/mask_RCNN/iou')
        maskRCNNResultSaver.saveResult(maskRCNNPairs, iouMaskRCNNResult, fileName)

        cv2.imwrite(OUT + '/' + str(index) + '_out.jpg', imgcv)

    yoloFinalStatistics = avarageStatistics(yoloAllStatistics)
    maskRcnnFinalStatistics = avarageStatistics(maskRcnnAllStatistics)

    saveFinalStatistics(yoloFinalStatistics)
    saveFinalStatistics(maskRcnnFinalStatistics)


def processYolo(index, imgcv):
    yoloReader = JsonReader('traffic', sortedYoloFileList[index], 'yolo')
    yoloBoundingBoxes = yoloReader.getBoundingBoxes()
    drawPredictedObjects(yoloBoundingBoxes, imgcv, BoxColors.CAR_COLOR, 2)
    showConfidence(yoloBoundingBoxes, imgcv, BoxColors.CAR_COLOR)
    return yoloBoundingBoxes


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


def saveFinalStatistics(statistics: Statistics):
    data = {}
    data['finalStatistics'] = []
    data['finalStatistics'].append({
        'alghorithmName': statistics.alghorithmName,
        'avgIoU': statistics.avgIoU,
        'mAP': statistics.mAP,
        'recall': statistics.recall,
        'precision': statistics.precision
    })
    with open(FINAL_STATISTICS + '/' + statistics.alghorithmName + '.json', 'w+') as outfile:
        json.dump(data, outfile)


run()
