import json
import itertools

class ResultSaver():
    def __init__(self, dir) -> None:
        self.dir = dir

    def saveResult(self, pairs, iouResults, fileName: str) -> None:
        data = {}
        data['frame'] = []
        for pair, iouResult in  zip(pairs, iouResults):
            data['frame'].append({
                'groundTruthBox': pair[0].__repr__(),
                'predictedBox': pair[1].__repr__(),
                'iou': iouResult
            })

        with open(self.dir +'/' +fileName.replace('jpg','json'), 'w+') as outfile:
            json.dump(data, outfile)
