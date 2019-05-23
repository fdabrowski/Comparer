import numpy as np
import os


class GtConverter():
    def __init__(self, projectName) -> None:
        self.__projectName = projectName
        self.__path = self.__createPath()

    def openFileForConvert(self):
        return open(self.__path + '/gt/gt.txt', 'r+')

    def __createPath(self):
        path = 'ground_truth_frames/' + self.__projectName
        if (os.path.isdir(path)):
            return path

    def convertFile(self):
        file = self.openFileForConvert()
        table = np.loadtxt(self.__path + '/gt/gt.txt', delimiter=",", dtype=float, usecols=(0, 1, 2, 3, 4, 5, 6, 7, 8))
        # sortedList = sorted(table, key=lambda l: l[0])
        length = int(table[len(table) - 1][0])
        for i in range(1, length):
            frameBoxes = list(filter(lambda x: x[0] == i, table))
            frameFile = open(self.__path + "/boxes/frame" + str(i - 1) + ".txt", "w+")
            for box in frameBoxes:
                gtValues = str(int(box[2])) + ' ' + str(int(box[3])) + ' ' + str(int(box[2]) + int(box[4])) + ' ' + str(int(box[3]) + int(box[5])) + ' person\n'
                frameFile.write(gtValues)
