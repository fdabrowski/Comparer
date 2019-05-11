from src.model.Statistics import Statistics


class StatisticsProvider():
    def __init__(self, alghorithmName, gtBoundingBoxes, predictedBoundingBoxes, pairs, iouResult) -> None:
        self.__alghorithmName = alghorithmName
        self.__gtBoundingBoxes = gtBoundingBoxes
        self.__predictedBoundingBoxes = predictedBoundingBoxes
        self.__pairs = pairs
        self.__iouResult = iouResult

    def __getPrecision(self):
        return self.__getTruePositives() / len(self.__predictedBoundingBoxes)

    def __getRecall(self):
        return self.__getTruePositives() / len(self.__gtBoundingBoxes)

    def average(self, list) -> float:
        return sum(list) / len(list)

    def __getTruePositives(self):
        inc = int()
        for pair in self.__pairs:
            if pair[1] is not None:
                inc += 1
        return inc

    def returnStatistics(self):
        return Statistics(
            self.__alghorithmName,
            self.average(self.__iouResult),
            0,
            self.__getRecall(),
            self.__getPrecision()
        )
