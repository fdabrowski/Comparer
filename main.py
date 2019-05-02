from os import listdir
from os.path import isfile, join

import cv2
import natsort

from src.GroundTruthReader import GroundTruthReader
from src.PairBox import PairBox
from src.YoloReader import YoloReader
from src.boxColors import BoxColors
from src.boxDrawer import drawPredictedObjects, showConfidence, drawRectangle

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
    showConfidence(yoloBoundingBoxes, imgcv, BoxColors.BICYCLE_COLOR)

    pairBox = PairBox()

    pairs = pairBox.findPredicted(gtBoundingBoxes, yoloBoundingBoxes)

    drawRectangle(pairs[2][0], imgcv, BoxColors.MOTOR_BIKE_COLOR, 10)
    drawRectangle(pairs[2][1], imgcv, BoxColors.MOTOR_BIKE_COLOR, 10)

    cv2.imwrite(OUT + str(index) + '_out.jpg', imgcv)

# box1 = BoundingBox(1,1,2,4, 'test')
# box2 = BoundingBox(1,2,2,4, 'test')
# iouProvider = IoUProvider()
# result = iouProvider.bb_intersection_over_union(box1, box2)
# print(result)
