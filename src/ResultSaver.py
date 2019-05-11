import json

from src.model import BoundingBox

class ResultSaver():
    def __init__(self, dir) -> None:
        self.dir = dir

    def saveResult(self, pairs, iouResults, fileName: str) -> None:
        data = {}
        data['frame'] = []
        for pair, iouResult in zip(pairs, iouResults):
            data['frame'].append({
                'groundTruthBox': self.toJSON(pair[0]),
                'predictedBox': self.toJSON(pair[1]),
                'iou': iouResult
            })

        with open(self.dir + '/' + fileName.replace('jpg', 'json'), 'w+') as outfile:
            json.dump(data, outfile)

    def toJSON(self, pair: BoundingBox):
        if (pair != None):
            return {
                'topleft_x': pair.topleft_x,
                'topleft_y': pair.topleft_y,
                'downright_x': pair.downright_x,
                'downright_y': pair.downright_y,
                'objectClass': pair.objectClass
            }
        else:
            return None

    def saveFinalStatistics(self):
        data = {}
        data['finalStatistics'] = []

        with open(self.dir + '/finalStatistics.json', 'w+') as outfile:
            json.dump(data, outfile)