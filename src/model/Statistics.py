class Statistics():
    def __init__(self, alghorithmName, mAP, recall, precision, time, class_recall) -> None:
        self.alghorithmName = alghorithmName
        self.mAP = mAP
        self.recall = recall
        self.precision = precision
        self.time = time
        self.class_recall = class_recall