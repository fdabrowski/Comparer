import os
from os import listdir
from os.path import isfile, join
import cv2
import natsort
from src.file_readers.GroundTruthReader import GroundTruthReader
from src.utils.boxColors import BoxColors
from src.utils.boxDrawer import drawPredictedObjects

TRAFFIC = 'traffic'
NIGHT_STREET = 'night_street'
ANIMALS = 'animals'

DARK = 'dark_'
LIGHT = 'light_'
BLUR = 'blur_'
PROJECT_NAME = ANIMALS

GT_FRAMES = 'ground_truth_frames/' + PROJECT_NAME + '/frames'
GT_BOXES = 'ground_truth_frames/' + PROJECT_NAME + '/boxes'
OUT = 'out/' + 'ground_truth/' + PROJECT_NAME
allGtFiles = [f for f in listdir(GT_BOXES) if isfile(join(GT_BOXES, f))]
allGtImages = [f for f in listdir(GT_FRAMES) if isfile(join(GT_FRAMES, f))]

if not os.path.exists(OUT):
    os.makedirs(OUT)

sortedGtFileList = natsort.natsorted(allGtFiles)
sortedGtImages = natsort.natsorted(allGtImages)

for index in range(0, len(sortedGtFileList)):
    fileName = sortedGtImages[index]
    imgcv = cv2.imread(GT_FRAMES + '/' + fileName)
    gtReader = GroundTruthReader(PROJECT_NAME, sortedGtFileList[index])
    gtBoundingBoxes = gtReader.getBoundingBoxes()
    drawPredictedObjects(gtBoundingBoxes, imgcv, BoxColors.GT_COLOR, 2)
    cv2.imwrite(OUT +'/' + str(index)  + '_out.jpg', imgcv)