from src.model.Statistics import Statistics

def avarageStatistics(statisticList):
    return Statistics(
        statisticList[0].alghorithmName,
        sum(statistics.mAP for statistics in statisticList) / float(len(statisticList)),
        sum(statistics.recall for statistics in statisticList) / float(len(statisticList)),
        sum(statistics.precision for statistics in statisticList) / float(len(statisticList)),

    )
