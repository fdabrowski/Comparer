import json
from src.BoundingBox import BoundingBox
from src.FileReader import FileReader


class YoloReader(FileReader):
    def __init__(self, projectName, fileName):
        super(YoloReader, self).__init__(projectName, fileName, 'yolo')

    def getBoundingBoxes(self):
        file = self.openBoxFile()
        return self.createBBList(file)

    def getBBValues(self, file):
        with open('data.txt') as json_file:
            data = json.load(json_file)
            for p in data['people']:
                print('Name: ' + p['name'])
                print('Website: ' + p['website'])
                print('From: ' + p['from'])
                print('')


    def createBBList(self, file):
        result = []
        bbList = self.getBBValues(file)
        for box in bbList:
            result.append(BoundingBox(int(box[0]), int(box[1]), int(box[2]), int(box[3]), box[4]))
        return result
