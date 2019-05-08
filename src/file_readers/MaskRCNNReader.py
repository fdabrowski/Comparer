from src.file_readers.JsonReader import JsonReader

class MaskRCNNReader(JsonReader):
    def __init__(self, projectName, fileName):
        super(JsonReader, self).__init__(projectName, fileName, 'mask_RCNN')
