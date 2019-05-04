import json

class ResultSaver():
    def __init__(self, dir) -> None:
        self.dir = dir

    def saveResult(self, pairs, iouResults, fileName: str) -> None:
        data = {}
        data['frame'] = []
        for pair, iouResult in pairs, iouResults:
            data['box'].append({
                'groundTruthBox': pair[0],
                'predictedBox': pair[1],
                'iou': iouResult
            })
        with open(self.dir +fileName + '.json', 'w+') as outfile:
            json.dump(data, outfile)
