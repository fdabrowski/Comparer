from os import listdir
from os.path import isfile, join
import cv2
import natsort
import matplotlib.pyplot as plt
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
gtAdapter = GroundTruthReader('traffic', 'frame0.txt')
boundingBoxes = gtAdapter.getBoundingBoxes()
drawPredictedObjects(boundingBoxes, imgcv)
imgplot = plt.imshow(imgcv)
plt.show()
