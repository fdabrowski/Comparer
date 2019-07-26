class BoundingBox():

    def __repr__(self) -> str:
        return '{topleft_x:' + str(self.topleft_x) + ', topleft_y:' +str(self.topleft_y) + ', downright_x:' +str(self.downright_x)+', downright_y:' +str(self.downright_y) +', object_class:' +str(self.object_class)


    def __init__(self, topleft_x, topleft_y, downRight_x, downRight_y, object_class):
        self.topleft_x = topleft_x
        self.topleft_y = topleft_y
        self.downright_x = downRight_x
        self.downright_y = downRight_y
        self.object_class = object_class