import matplotlib.pyplot as plt
from numpy.ma import arange
import numpy as np
from graph_data import GraphData

yolo_dir = 'yolo/'
rcnn_dir = 'rcnn/'
ssd_dir = 'ssd/'

def add_empty(x_complex, available_classes):
    for clazz in available_classes:
        x_complex.append(GraphData(clazz))

def get_recall_data(statistics, available_classes, alg_name):
    x_complex = []
    add_empty(x_complex, available_classes)
    for statistic in statistics:
        for index, clazz in enumerate(available_classes):
            for single_recall in statistic.class_recall:
                if single_recall.class_name == clazz:
                    x_complex[index].is_nullable = False
                    x_complex[index].items.append(single_recall.recall)
    for item in x_complex:
        if item.is_nullable:
            x_complex.remove(item)

    plt.figure(num=None, figsize=(14, 7), dpi=80, facecolor='w', edgecolor='k')
    plt.rcParams.update({'font.size': 20})
    plt.subplot(111)
    x_range = list(arange(1, len(x_complex[0].items) + 1, 1.0))
    x = np.array(x_range)
    plt.bar(x - 0.3, x_complex[0].items, width=0.6, fill=True, label=x_complex[0].class_name, align='center')
    plt.bar(x + 0.3, x_complex[1].items, width=0.6, fill=True, label=x_complex[1].class_name, align='center')
    plt.xlabel('Numer klatki', fontsize=20)
    plt.ylabel('Pokrycie', fontsize=20)
    plt.title('Pokrycie w poszczególnych klatkach - ' + alg_name, fontsize=20)
    plt.xticks(np.arange(0, len(x), 10))
    # handles, labels = plt.get_legend_handles_labels()
    plt.legend(prop={'size': 20})
    plt.show()