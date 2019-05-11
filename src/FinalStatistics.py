import numpy as np

from src.model.Statistics import Statistics


def avarageStatistics(statisticList):
    return Statistics(
        statisticList[0].alghorithmName,
        # np.mean(statistics.avgIoU for statistics in statisticList),
        # np.mean(statistics.mAP for statistics in statisticList),
        # np.mean(statistics.recall for statistics in statisticList),
        # np.mean(statistics.precision for statistics in statisticList),
        sum(statistics.avgIoU for statistics in statisticList) / float(len(statisticList)),
        sum(statistics.mAP for statistics in statisticList) / float(len(statisticList)),
        sum(statistics.recall for statistics in statisticList) / float(len(statisticList)),
        sum(statistics.precision for statistics in statisticList) / float(len(statisticList)),

    )
