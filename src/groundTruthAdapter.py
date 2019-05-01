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

    def getFileContent(self):
        file = self.openLabelsFile()
        boundingBoxesList = self.createBBList(file)
        print(boundingBoxesList)

    def createPath(self):
        path = '../' + self.dirName + '/' + self.projectName + '/labels'
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
            result.append(BoundingBox(box[0], box[1], box[2], box[3], box[4]))
        return result