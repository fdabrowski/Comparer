class BoundingBox():
    def __init__(self, topleft_x, topleft_y, downRight_x, downRight_y, objectClass):
        self.topleft_x = topleft_x
        self.topleft_y = topleft_y
        self.downright_x = downRight_x
        self.downright_y = downRight_y
        self.objectClass = objectClass