import os
from os import listdir
from os.path import isfile, join
from shutil import copyfile

PROJECT_NAME = 'Bird_Cat_Dog'
DIR = '/Users/filipdabrowski/Documents/git/OIDv4_ToolKit/OID/Dataset/train/' + PROJECT_NAME
LABELS = DIR + '/Label'
OUT = DIR + '/filtered'
OUT_LABELS = OUT + '/label'
CONVERTED_LABELS = OUT + '/boxes'

if not os.path.exists(CONVERTED_LABELS):
    os.makedirs(CONVERTED_LABELS)

all_files = [f for f in listdir(OUT_LABELS) if isfile(join(OUT_LABELS, f))]

for fileName in all_files:
    new_file = open(CONVERTED_LABELS + '/' + fileName, "w+")
    file = open(OUT_LABELS + '/' + fileName, 'r+')
    for line in file:
        boxList = line.split()
        new_file.write(boxList[1] + ' ' + boxList[2] + ' ' + boxList[3] + ' ' + boxList[4] + ' ' + boxList[0] + '\n')
