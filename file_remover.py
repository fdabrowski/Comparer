import os
from os import listdir
from os.path import isfile, join
from shutil import copyfile

PROJECT_NAME = 'Apple_Banana_Orange'
DIR = '/Users/filipdabrowski/Documents/git/OIDv4_ToolKit/OID/Dataset/train/' + PROJECT_NAME
LABELS = DIR + '/Label'
OUT = DIR + '/filtered'
OUT_LABELS = OUT + '/label'

if not os.path.exists(OUT):
    os.makedirs(OUT)

if not os.path.exists(OUT_LABELS):
    os.makedirs(OUT_LABELS)

all_files = [f for f in listdir(LABELS) if isfile(join(LABELS, f))]

for file in all_files:
    image_name = file.replace('.txt', '.jpg')
    image_path = DIR + '/' + image_name
    label_path = LABELS + '/' + file
    num_lines = sum(1 for line in open(label_path))
    print(num_lines)
    if num_lines > 5:
        copyfile(image_path, OUT + '/' + image_name)
        copyfile(label_path, OUT_LABELS + '/' + file)
