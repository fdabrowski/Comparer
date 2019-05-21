import json
from src.model.BoundingBox import BoundingBox
from src.file_readers.FileReader import FileReader


class JsonReader(FileReader):
    def __init__(self, projectName, fileName, folderName):
        super(JsonReader, self).__init__(projectName, fileName, folderName)

    def getBoundingBoxes(self):
        file = self.openBoxFile()
        return self.createBBList(file)

    def getTime(self):
        file = self.openTimeFile()
        return self.__getTimeFromJSON(file)

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

    def __getTimeFromJSON(self, file):
        data = json.load(file)
        return data[0]['time']
