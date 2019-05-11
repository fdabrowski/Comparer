class Statistics():
    def __init__(self, alghorithmName, avgIoU, mAP, recall, precision) -> None:
        self.alghorithmName = alghorithmName
        self.avgIoU = avgIoU
        self.mAP = mAP
        self.recall = recall
        self.precision = precision
        self.time = 10