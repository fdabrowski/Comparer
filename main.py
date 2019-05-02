from os import listdir
from os.path import isfile, join
import cv2
import natsort
import matplotlib.pyplot as plt

from src.YoloReader import YoloReader
from src.boxDrawer import drawPredictedObjects
from src.GroundTruthReader import GroundTruthReader

GT_FRAMES = '../ground_truth_frames/traffic/frames'
GT_BOXES = '../ground_truth_frames/traffic/boxes'
allFiles = [f for f in listdir(GT_BOXES) if isfile(join(GT_BOXES, f))]
sortedFileList = natsort.natsorted(allFiles)
allBoundingBox = []

# for fileName in sortedFileList:
#     gtAdapter = GroundTruthAdapter('traffic', fileName)
#     allBoundingBox.append(gtAdapter.getBoundingBoxes())


#
imgcv = cv2.imread(GT_FRAMES +'/frame0.jpg')

# gtReader = GroundTruthReader('traffic', 'frame0.txt')
# gtBoundingBoxes = gtReader.getBoundingBoxes()
# drawPredictedObjects(gtBoundingBoxes, imgcv)

yoloReader = YoloReader('traffic', 'frame1.json')
yoloBoundingBoxes = yoloReader.getBoundingBoxes()
drawPredictedObjects(yoloBoundingBoxes, imgcv)

imgplot = plt.imshow(imgcv)
plt.show()
