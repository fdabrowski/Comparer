from src.model.Statistics import Statistics


class StatisticsProvider():
    def __init__(self, alghorithmName, gtBoundingBoxes, predictedBoundingBoxes, pairs, iouResult, time) -> None:
        self.__alghorithmName = alghorithmName
        self.__gtBoundingBoxes = gtBoundingBoxes
        self.__predictedBoundingBoxes = predictedBoundingBoxes
        self.__pairs = pairs
        self.__iouResult = iouResult
        self.__time = time

    def __getPrecision(self):
        if (len(self.__predictedBoundingBoxes) is not 0):
            return self.__getTruePositives() / len(self.__predictedBoundingBoxes)
        else:
            return 0


    def __getRecall(self):
        return self.__getTruePositives() / len(self.__gtBoundingBoxes)

    def average(self, list) -> float:
        if(len(list) is not 0):
            return sum(list) / len(list)
        else:
            return 0

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
            self.__getRecall(),
            self.__getPrecision(),
            self.__time
        )
