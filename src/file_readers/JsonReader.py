import json
from src.model.BoundingBox import BoundingBox
from src.file_readers.FileReader import FileReader


class JsonReader(FileReader):
    def __init__(self, project_name, file_name, folderName):
        super(JsonReader, self).__init__(project_name, file_name, folderName)

    def getBoundingBoxes(self):
        file = self.open_box_file()
        return self.createBBList(file)

    def getTime(self):
        file = self.open_time_file()
        return self.__getTimeFromJSON(file)

    def createBBList(self, file):
            data = json.load(file)
            result = []
            for box in data:
                if box['label'] == 'wine':
                    box['label'] = box['label'].replace('wine', 'wine glass')
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
