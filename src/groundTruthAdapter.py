import os

class GroundTruthAdapter():
    def __init__(self, projectName, fileName):
        self.fileName = fileName
        self.projectName = projectName
        self.path = self.createPath()
        self.dirName = 'ground_truth_frames'

    def openLabelsFile(self):
        filePath = self.path +'/' + self.fileName
        if(os.path.isfile(filePath))
            self.file = open(filePath)
            print(self.file)

    def createPath(self):
        path = self.dirName +'/' +self.projectName +'/labels'
        if(os.path.isdir(path)):
            return path
