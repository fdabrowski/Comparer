from src.model.BoundingBox import BoundingBox

class IoUProvider():

    def __init__(self) -> None:
        super().__init__()

    def bbIntersectionOverUnion(self, gtBB: BoundingBox, predictedBB: BoundingBox) -> float:

        interArea = self.getInterArea(gtBB, predictedBB)

        boxAArea = (gtBB.downright_x - gtBB.topleft_x + 1) * (gtBB.downright_y - gtBB.topleft_y + 1)
        boxBArea = (predictedBB.downright_x - predictedBB.topleft_x + 1) * (
                    predictedBB.downright_y - predictedBB.topleft_y + 1)

        iou = interArea / float(boxAArea + boxBArea - interArea)

        return iou

    def getInterArea(self, gtBB: BoundingBox, predictedBB: BoundingBox):
        xA = max(gtBB.topleft_x, predictedBB.topleft_x)
        yA = max(gtBB.topleft_y, predictedBB.topleft_y)
        xB = min(gtBB.downright_x, predictedBB.downright_x)
        yB = min(gtBB.downright_y, predictedBB.downright_y)

        return max(0, xB - xA + 1) * max(0, yB - yA + 1)

    def getIouResult(self, pairs):
        result = []
        for pair in pairs:
            if (pair[0] != None and pair[1] != None):
                result.append(self.bbIntersectionOverUnion(pair[0], pair[1]))
        return result
