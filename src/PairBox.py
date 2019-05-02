import numpy as np

from src import BoundingBox
from src.IoUProvider import IoUProvider


class PairBox():
    def __init__(self) -> None:
        super().__init__()

    def findPredicted(self, gtBoundingBoxes, predictedBoundingBox):
        result = []
        iouProvider = IoUProvider()
        for gtBox in gtBoundingBoxes:
            potencialBoxes = []
            for predictedBox in predictedBoundingBox:
                if (self.__ifPotencialPair(iouProvider, gtBox, predictedBox) > 0):
                    potencialBoxes.append(predictedBox)
            if (len(potencialBoxes) == 1):
                result.append([gtBox, potencialBoxes[0]])
            elif (len(potencialBoxes) == 0):
                result.append([gtBox, None])
            else:
                result.append(self.__getClosest(gtBox, potencialBoxes))
        return result

    def __getClosest(self, gtBox: BoundingBox, potencialBoxes) -> BoundingBox:
        result = [gtBox, potencialBoxes[0]]
        for box in potencialBoxes:
            if (self.__getDistance(gtBox, box) < self.__getDistance(gtBox, potencialBoxes[0])):
                result[1] = box
        return result

    def __getDistance(self, gtBox, box) -> float:
        return np.sqrt(np.square(box.topleft_x - gtBox.topleft_x) + np.square(box.topleft_y - gtBox.topleft_y))

    def __ifPotencialPair(self, iouProvider: IoUProvider, gtBox: BoundingBox, predictedBox: BoundingBox) -> bool:
        return iouProvider.getInterArea(gtBox, predictedBox) > 0 and gtBox.objectClass == predictedBox.objectClass
