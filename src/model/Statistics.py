class Statistics():
    def __init__(self, alghorithmName, mAP, recall, precision) -> None:
        self.alghorithmName = alghorithmName
        self.mAP = mAP
        self.recall = recall
        self.precision = precision
        self.time = 10