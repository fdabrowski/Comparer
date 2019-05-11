import json

from src.model.Statistics import Statistics

def avarageStatistics(statisticList):
    return Statistics(
        statisticList[0].alghorithmName,
        sum(statistics.mAP for statistics in statisticList) / float(len(statisticList)),
        sum(statistics.recall for statistics in statisticList) / float(len(statisticList)),
        sum(statistics.precision for statistics in statisticList) / float(len(statisticList)),

    )

def saveFinalStatistics(dir: str, statistics: Statistics):
    data = {}
    data['finalStatistics'] = []
    data['finalStatistics'].append({
        'alghorithmName': statistics.alghorithmName,
        'mAP': statistics.mAP,
        'recall': statistics.recall,
        'precision': statistics.precision
    })
    with open(dir + '/' + statistics.alghorithmName + '.json', 'w+') as outfile:
        json.dump(data, outfile)
