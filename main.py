from os import listdir
from os.path import isfile, join

import cv2
import matplotlib.pyplot as plt
import natsort

from src.GroundTruthReader import GroundTruthReader
from src.YoloReader import YoloReader
from src.boxColors import BoxColors
from src.boxDrawer import drawPredictedObjects

GT_FRAMES = '../ground_truth_frames/traffic/frames'
GT_BOXES = '../ground_truth_frames/traffic/boxes'

YOLO_FRAMES = '../yolo/traffic/frames'
YOLO_BOXES = '../yolo/traffic/boxes'

OUT = '../out/traffic'

allGtFiles = [f for f in listdir(GT_BOXES) if isfile(join(GT_BOXES, f))]
allGtImages = [f for f in listdir(GT_FRAMES) if isfile(join(GT_FRAMES, f))]
allYoloFIles = [f for f in listdir(YOLO_BOXES) if isfile(join(YOLO_BOXES, f))]

sortedGtFileList = natsort.natsorted(allGtFiles)
sortedGtImages = natsort.natsorted(allGtImages)
sortedYoloFileList = natsort.natsorted(allYoloFIles)

allBoundingBox = []

for index in range(0, len(sortedGtFileList)):
    imgcv = cv2.imread(GT_FRAMES + '/' + sortedGtImages[index])

    gtReader = GroundTruthReader('traffic', sortedGtFileList[index])
    gtBoundingBoxes = gtReader.getBoundingBoxes()
    drawPredictedObjects(gtBoundingBoxes, imgcv, BoxColors.TRUCK_COLOR, 2)

    yoloReader = YoloReader('traffic', sortedYoloFileList[index])
    yoloBoundingBoxes = yoloReader.getBoundingBoxes()
    drawPredictedObjects(yoloBoundingBoxes, imgcv, BoxColors.BICYCLE_COLOR, 3)

    cv2.imwrite(OUT + str(index) + '_out.jpg', imgcv)



