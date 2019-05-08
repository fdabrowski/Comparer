from os import listdir
from os.path import isfile, join

import cv2
import natsort

from src.IoUProvider import IoUProvider
from src.ResultSaver import ResultSaver
from src.file_readers.JsonReader import JsonReader
from src.PairBox import PairBox
from src.file_readers.GroundTruthReader import GroundTruthReader
from src.file_readers.MaskRCNNReader import MaskRCNNReader
from src.file_readers.JsonReader import JsonReader
from src.utils.boxColors import BoxColors
from src.utils.boxDrawer import drawPredictedObjects, showConfidence, drawRectangle, markPairedBoxes

GT_FRAMES = '../ground_truth_frames/traffic/frames'
GT_BOXES = '../ground_truth_frames/traffic/boxes'

MASK_RCNN_BOXES = '../mask_RCNN/traffic/boxes'
MASK_RCNN_FRAMES = '../mask_RCNN/traffic/frames'

YOLO_FRAMES = '../yolo/traffic/frames'
YOLO_BOXES = '../yolo/traffic/boxes'

OUT = '../out/traffic'

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
    for index in range(0, len(sortedGtFileList)):
        fileName = sortedGtImages[index]
        imgcv = cv2.imread(GT_FRAMES + '/' + fileName)

        gtReader = GroundTruthReader('traffic', sortedGtFileList[index])
        gtBoundingBoxes = gtReader.getBoundingBoxes()
        drawPredictedObjects(gtBoundingBoxes, imgcv, BoxColors.GT_COLOR, 2)

        yoloReader = JsonReader('traffic', sortedYoloFileList[index], 'yolo')
        yoloBoundingBoxes = yoloReader.getBoundingBoxes()
        drawPredictedObjects(yoloBoundingBoxes, imgcv, BoxColors.CAR_COLOR, 2)
        showConfidence(yoloBoundingBoxes, imgcv, BoxColors.CAR_COLOR)

        rcnnReader = JsonReader('traffic', sortedMaskRCNNFileList[index], 'mask_RCNN')
        rcnnBoundingBox = rcnnReader.getBoundingBoxes()
        drawPredictedObjects(rcnnBoundingBox, imgcv, BoxColors.RCNN_COLOR, 2)
        showConfidence(rcnnBoundingBox, imgcv, BoxColors.RCNN_COLOR)

        yoloPairBox = PairBox()
        yoloPairs = yoloPairBox.findPredicted(gtBoundingBoxes, yoloBoundingBoxes)

        maskRCNNPairBox = PairBox()
        maskRCNNPairs = maskRCNNPairBox.findPredicted(gtBoundingBoxes, rcnnBoundingBox)

        iouProvider = IoUProvider()
        iouYoloResult = iouProvider.getIouResult(yoloPairs)
        iouMaskRCNNResult = iouProvider.getIouResult(maskRCNNPairs)

        # markPairedBoxes(imgcv, pairs)

        yoloResultSaver = ResultSaver(OUT +'/yolo/iou')
        yoloResultSaver.saveResult(yoloPairs, iouYoloResult, fileName)

        maskRCNNResultSaver = ResultSaver(OUT + '/mask_RCNN/iou')
        maskRCNNResultSaver.saveResult(maskRCNNPairs, iouMaskRCNNResult, fileName)

        cv2.imwrite(OUT +'/' + str(index) + '_out.jpg', imgcv)

    # box1 = BoundingBox(1,1,2,4, 'test')
    # box2 = BoundingBox(1,2,2,4, 'test')
    # iouProvider = IoUProvider()
    # result = iouProvider.bb_intersection_over_union(box1, box2)
    # print(result)





run()