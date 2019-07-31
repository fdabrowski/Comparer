from enum import Enum

class LabelSource(Enum):
    open_images = 'open_images'
    cvat = 'cvat'
    bbox = 'bbox'