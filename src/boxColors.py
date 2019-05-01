class BoxColors:
    DOG_COLOR = (0, 255, 0)
    CAT_COLOR = (0, 0, 255)
    TRUCK_COLOR = (255, 0, 255)
    MOTOR_BIKE_COLOR = (255, 0, 0)
    BICYCLE_COLOR = (255, 255, 255)

    def setColorForClass(self, label):
        if (label == 'cat'):
            return self.CAT_COLOR
        elif (label == 'dog'):
            return self.DOG_COLOR
        elif (label == 'motorbike'):
            return self.MOTOR_BIKE_COLOR
        elif (label == 'truck'):
            return self.TRUCK_COLOR
        elif (label == 'bicycle'):
            return self.BICYCLE_COLOR