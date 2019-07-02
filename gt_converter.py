import numpy as np
import os


class GtConverter():
    def __init__(self, project_name) -> None:
        self.__project_name = project_name
        self.__path = self.__create_path()

    def open_file_for_convert(self):
        return open(self.__path + '/gt/gt.txt', 'r+')

    def __create_path(self):
        path = 'ground_truth_frames/' + self.__project_name
        if (os.path.isdir(path)):
            return path

    def convert_file(self):
        file = self.open_file_for_convert()
        table = np.loadtxt(self.__path + '/gt/gt.txt', delimiter=",", dtype=float, usecols=(0, 1, 2, 3, 4, 5, 6, 7, 8))
        # sortedList = sorted(table, key=lambda l: l[0])
        length = int(table[len(table) - 1][0])
        for i in range(1, length):
            frame_boxes = list(filter(lambda x: x[0] == i, table))
            frame_file = open(self.__path + "/boxes/frame" + str(i - 1) + ".txt", "w+")
            for box in frame_boxes:
                gt_values = str(int(box[2])) + ' ' + str(int(box[3])) + ' ' + str(int(box[2]) + int(box[4])) + ' ' + str(int(box[3]) + int(box[5])) + ' person\n'
                frame_file.write(gt_values)
