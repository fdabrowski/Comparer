import copy

import numpy as np

from src.model import BoundingBox
from src.IoUProvider import IoUProvider


class PairBox():
    def __init__(self) -> None:
        super().__init__()

    def find_predicted(self, gtBoundingBoxes, predicted_bounding_box):
        result = []
        predicted_copy = copy.copy(predicted_bounding_box)
        iouProvider = IoUProvider()
        for gtBox in gtBoundingBoxes:
            potencialBoxes = []
            for predictedBox in predicted_copy:
                if (self.__if_potencial_pair(iouProvider, gtBox, predictedBox) > 0):
                    potencialBoxes.append(predictedBox)
            if (len(potencialBoxes) == 1):
                result.append([gtBox, potencialBoxes[0]])
                predicted_copy.remove(potencialBoxes[0])
            elif (len(potencialBoxes) == 0):
                result.append([gtBox, None])
            else:
                closest_box = self.__get_closest(gtBox, potencialBoxes)
                result.append(closest_box)
                predicted_copy.remove(closest_box[1])
        return result

    def __get_closest(self, gtBox: BoundingBox, potencialBoxes) -> BoundingBox:
        result = [gtBox, potencialBoxes[0]]
        for box in potencialBoxes:
            if (self.__get_distance(gtBox, box) < self.__get_distance(gtBox, potencialBoxes[0])):
                result[1] = box
        return result

    def __get_distance(self, gtBox, box) -> float:
        return np.sqrt(np.square(box.topleft_x - gtBox.topleft_x) + np.square(box.topleft_y - gtBox.topleft_y))

    def __if_potencial_pair(self, iouProvider: IoUProvider, gtBox: BoundingBox, predictedBox: BoundingBox) -> bool:
        predictedBox.objectClass = predictedBox.objectClass.replace('wine_glass', 'wine glass')
        return iouProvider.getInterArea(gtBox, predictedBox) > 0 and gtBox.objectClass.lower() == predictedBox.objectClass.lower()
