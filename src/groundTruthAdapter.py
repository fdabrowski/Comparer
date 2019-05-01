import os

from src.BoundingBox import BoundingBox


class GroundTruthAdapter():
    def __init__(self, projectName, fileName):
        self.fileName = fileName
        self.projectName = projectName
        self.dirName = 'ground_truth_frames'
        self.path = self.createPath()

    def openLabelsFile(self):
        filePath = self.path + '/' + self.fileName
        if (os.path.isfile(filePath)):
            return open(filePath, 'r+')

    def getBoundingBoxes(self):
        file = self.openLabelsFile()
        return self.createBBList(file)

    def createPath(self):
        path = '../' +self.dirName + '/' + self.projectName + '/boxes'
        if (os.path.isdir(path)):
            return path
        else:
            return ''

    def getBBValues(self, file):
        result = []
        for line in file:
            boxList = line.split()
            result.append(boxList)
        result.pop(0)
        return result

    def createBBList(self, file):
        result = []
        bbList = self.getBBValues(file)
        for box in bbList:
            result.append(BoundingBox(int(box[0]), int(box[1]), int(box[2]), int(box[3]), box[4]))
        return result