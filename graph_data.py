class GraphData():
    def __init__(self, class_name) -> None:
        self.class_name = class_name
        self.is_nullable = True
        self.items = []
        super().__init__()