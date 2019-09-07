import json
from src.model import BoundingBox
import os

class ResultSaver():
    def __init__(self, dir) -> None:
        self.dir = self.__setDir(dir)

    def save_result(self, pairs, iouResults, fileName: str, statistics) -> None:
        data = {}
        data['statistics'] = []
        data['frame'] = []
        for pair, iouResult in zip(pairs, iouResults):
            data['frame'].append({
                'groundTruthBox': self.toJSON(pair[0]),
                'predictedBox': self.toJSON(pair[1]),
                'iou': iouResult
            })
        data['statistics'].append({
            'alghorithmName': statistics.alghorithmName,
            'class_recall': list(map(lambda x: {'class_name': x.class_name, 'recall': x.recall}, statistics.class_recall)),
            'mAp': statistics.mAP,
            'precision': statistics.precision,
            'recall': statistics.recall,
            'time': statistics.time
        })
        with open(self.dir + '/' + fileName.replace('jpg', 'json'), 'w+') as outfile:
            json.dump(data, outfile)

    def __setDir(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)
        return dir

    def toJSON(self, pair: BoundingBox):
        if (pair != None):
            return {
                'topleft_x': pair.topleft_x,
                'topleft_y': pair.topleft_y,
                'downright_x': pair.downright_x,
                'downright_y': pair.downright_y,
                'object_class': pair.object_class
            }
        else:
            return None
