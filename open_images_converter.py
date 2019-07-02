import cv2
import os
from os import listdir
from os.path import isfile, join

import natsort

from videoCreator import VIDEO_HEIGHT, VIDEO_WIDTH

PROJECT_NAME = 'Bird_Cat_Dog'
DIR = '/Users/filipdabrowski/Documents/git/OIDv4_ToolKit/OID/Dataset/train/' + PROJECT_NAME
LABELS = DIR + '/Label'
OUT = DIR + '/filtered'
OUT_LABELS = OUT + '/label'
CONVERTED_LABELS = '/Users/filipdabrowski/Documents/git/Comparer/ground_truth_frames/animals/boxes'


def get_height_and_width(file_name: str):
    imgcv = cv2.imread(OUT + '/' + file_name.replace('txt', 'jpg'))
    height, width, layers = imgcv.shape
    return VIDEO_HEIGHT/height, VIDEO_WIDTH/width


if not os.path.exists(CONVERTED_LABELS):
    os.makedirs(CONVERTED_LABELS)

all_files = [f for f in listdir(OUT_LABELS) if isfile(join(OUT_LABELS, f))]
sorted_all_files = natsort.natsorted(all_files)

for index in range(0, len(sorted_all_files)):
    new_file = open(CONVERTED_LABELS + '/frame' + str(index) + '.txt', "w+")
    file = open(OUT_LABELS + '/' + sorted_all_files[index], 'r+')
    height_rate, width_rate = get_height_and_width(sorted_all_files[index])
    new_file.write(str(sum(1 for line in file)) + '\n')
    file.seek(0)
    for line in file:
        boxList = line.split()
        new_file.write(str(int(float(boxList[1])*width_rate)) + ' '
                       + str(int(float(boxList[2])*height_rate)) + ' '
                       + str(int(float(boxList[3])*width_rate)) + ' '
                       + str(int(float(boxList[4])*height_rate)) + ' '
                       + boxList[0] + '\n')
        # new_file.write(boxList[1]+ ' '
        #                + boxList[2] + ' '
        #                + boxList[3] + ' '
        #                + boxList[4] + ' '
        #                + boxList[0] + '\n')

