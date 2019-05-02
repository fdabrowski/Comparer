from src.model.BoundingBox import BoundingBox
from src.file_readers.FileReader import FileReader


class GroundTruthReader(FileReader):
    def __init__(self, projectName, fileName):
        super(GroundTruthReader, self).__init__(projectName, fileName, 'ground_truth_frames')

    def getBoundingBoxes(self):
        file = self.openBoxFile()
        return self.createBBList(file)

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