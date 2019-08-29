from random import randrange
from typing import List

import matplotlib.pyplot as plt

from graph_data import GraphData
from src.model import Statistics



yolo_dir = 'yolo/'
rcnn_dir = 'rcnn/'
ssd_dir = 'ssd/'

def add_empty(x_complex, available_classes):
    for clazz in available_classes:
        x_complex.append(GraphData(clazz))

def get_recall_data(statistics, available_classes):
    x_complex = []
    add_empty(x_complex, available_classes)
    for statistic in statistics:
        for single_recall in statistic.class_recall:
            for index, clazz in enumerate(available_classes):
                if single_recall.class_name == clazz:
                    x_complex[index].is_nullable = False
                    x_complex[index].items.append(single_recall.recall)
                else:
                    x_complex[index].items.append(None)
    for item in x_complex:
        if item.is_nullable:
            x_complex.remove(item)

    colors = ['blue', 'red', 'orange']
    markers = ['^', 'o', 'x', '+']
    plt.figure(num=None, figsize=(14, 7), dpi=80, facecolor='w', edgecolor='k')
    for item in x_complex:
        x = list(range(1, len(item.items)+1))
        y = item.items
        plt.scatter(x, y, marker=markers[randrange(2)], color=colors[randrange(2)], s=10 )
    plt.xlabel('Numer klatki')
    plt.ylabel('Pokrycie w danej klatce')
    plt.show()