import json
import os
from typing import List

from src.StatisticsProvider import ClassRecall
from src.model.Statistics import Statistics

def avarage_statistics(statisticList: List[Statistics], available_classes):
    return Statistics(
        statisticList[0].alghorithmName,
        sum(statistics.mAP for statistics in statisticList) / float(len(statisticList)),
        sum(statistics.recall for statistics in statisticList) / float(len(statisticList)),
        sum(statistics.precision for statistics in statisticList) / float(len(statisticList)),
        statisticList[0].time,
        get_class_recall(statisticList, available_classes)

    )

def save_final_statistics(dir: str, statistics: Statistics):
    data = {}
    data['finalStatistics'] = []
    data['finalStatistics'].append({
        'alghorithmName': statistics.alghorithmName,
        'mAP': statistics.mAP,
        'recall': statistics.recall,
        'precision': statistics.precision,
        'time': statistics.time
    })
    if not os.path.exists(dir):
        os.makedirs(dir)
    with open(dir + '/' + statistics.alghorithmName + '.json', 'w+') as outfile:
        json.dump(data, outfile)

def get_class_recall(statistics_list: List[Statistics], available_classes):
    class_recall = []
    class_recalls_list_unmerged = list(map(lambda x: x.class_recall, statistics_list))
    concated_list = []
    for class_recall_list in class_recalls_list_unmerged:
        concated_list = concated_list + class_recall_list
    for sing_class in available_classes:
        class_recall_list = list(filter(lambda class_recall: class_recall.class_name == sing_class, concated_list))
        if len(class_recall_list) > 0:
            recall_list = list(map(lambda x: x.recall, class_recall_list))
            class_recall.append(ClassRecall(sing_class, sum(recall_list) / len(class_recall_list)))
    return class_recall