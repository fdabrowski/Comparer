from src.model.BoundingBox import BoundingBox
from src.file_readers.FileReader import FileReader


class GroundTruthReader(FileReader):
    def __init__(self, project_name, video_name, file_name):
        super(GroundTruthReader, self).__init__(project_name, video_name, file_name, 'ground_truth_frames')

    def getBoundingBoxes(self):
        file = self.open_box_file()
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
            result.append(BoundingBox(int(float(box[0])), int(float(box[1])), int(float(box[2])), int(float(box[3])), box[4]))
        return result