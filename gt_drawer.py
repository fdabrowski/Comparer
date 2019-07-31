import os
from os import listdir
from os.path import isfile, join
import cv2
import natsort
from src.file_readers.GroundTruthReader import GroundTruthReader
from src.utils.boxColors import BoxColors
from src.utils.boxDrawer import draw_predicted_objects, show_confidence

TRAFFIC = 'traffic'
NIGHT_STREET = 'night_street'
ANIMALS = 'animals'
PERSON = 'person'
GLASS = 'glass'
BIKE = 'bike'
HORSE_2 = 'horse2'

DARK = 'dark_'
LIGHT = 'light_'
BLUR = 'blur_'

PROJECT_NAME = HORSE_2

GT_FRAMES = 'ground_truth_frames/' + PROJECT_NAME + '/frames'
# GT_BOXES = 'ground_truth_frames/' + PROJECT_NAME + '/boxes'
GT_BOXES = 'ssd/' + PROJECT_NAME + '/boxes'
OUT = 'out/' + 'ground_truth/ssd' + PROJECT_NAME
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
    draw_predicted_objects(gtBoundingBoxes, imgcv, BoxColors.GT_COLOR, 2)
    show_confidence(gtBoundingBoxes, imgcv, BoxColors.GT_COLOR)
    cv2.imwrite(OUT +'/' + str(index)  + '_out.jpg', imgcv)