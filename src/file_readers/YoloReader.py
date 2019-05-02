import json
from src.model.BoundingBox import BoundingBox
from src.file_readers.FileReader import FileReader


class YoloReader(FileReader):
    def __init__(self, projectName, fileName):
        super(YoloReader, self).__init__(projectName, fileName, 'yolo')

    def getBoundingBoxes(self):
        file = self.openBoxFile()
        return self.createBBList(file)

    def createBBList(self, file):
            data = json.load(file)
            result = []
            for box in data:
                result.append(
                    BoundingBox(
                        int(box['topleft']['x']),
                        int(box['topleft']['y']),
                        int(box['bottomright']['x']),
                        int(box['bottomright']['y']),
                        box['label']))
            return result
