import json

from src.model.Statistics import Statistics

class ClassRecall():

    def __init__(self, class_name: str, recall: float) -> None:
        self.class_name = class_name
        self.recall = recall
        super().__init__()

    def toJSON(self):
        return json.dumps(self)



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
            return self.__getTruePositives(self.__pairs) / len(self.__predictedBoundingBoxes)
        else:
            return 0


    def __getRecall(self):
        return self.__getTruePositives(self.__pairs) / len(self.__gtBoundingBoxes)

    def average(self, list) -> float:
        if(len(list) is not 0):
            return sum(list) / len(list)
        else:
            return 0

    def __getTruePositives(self, pairs):
        inc = int()
        for pair in pairs:
            if pair[1] is not None:
                inc += 1
        return inc

    def __get_class_recall(self):
        class_recall = []
        classes_list = list(set(map(lambda box: box.object_class, self.__gtBoundingBoxes)))
        for sing_class in classes_list:
            class_pairs = list(filter(lambda pair: pair[0].object_class == sing_class, self.__pairs))
            true_positive = self.__getTruePositives(class_pairs)
            class_recall.append(ClassRecall(sing_class, true_positive / len(class_pairs)))
        return class_recall

    def returnStatistics(self):
        return Statistics(
            self.__alghorithmName,
            self.average(self.__iouResult),
            self.__getRecall(),
            self.__getPrecision(),
            self.__time,
            self.__get_class_recall()
        )
