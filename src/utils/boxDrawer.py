from cv2 import cv2

from src.utils.boxColors import BoxColors

font = cv2.QT_FONT_NORMAL
fontScale = 1
fontColor = (0, 0, 0)
lineType = 2

DOG_COLOR = (0, 255, 0)
CAT_COLOR = (0, 0, 255)
TRUCK_COLOR = (255, 0, 255)
MOTOR_BIKE_COLOR = (255, 0, 0)
BICYCLE_COLOR = (255, 255, 255)


def drawPredictedObjects(result, img, color, width):
    for box in result:
        drawRectangle(box, img, color, width)

def drawRectangle(box, img, color, width):
    if(box != None):
        cv2.rectangle(img,
                      (box.topleft_x, box.topleft_y),
                      (box.downright_x, box.downright_y),
                      color,
                      width)

def showConfidence(result, img, color):
    for box in result:
        text = box.objectClass
        (text_width, text_height) = cv2.getTextSize(text, font, fontScale=fontScale, thickness=1)[0]
        text_offset_x = box.topleft_x
        text_offset_y = box.topleft_y
        # make the coords of the box with a small padding of two pixels
        box_coords = ((text_offset_x, text_offset_y), (text_offset_x + text_width - 2, text_offset_y - text_height - 2))
        cv2.rectangle(img, box_coords[0], box_coords[1], color, cv2.FILLED)
        cv2.putText(img,
                    text,
                    (box.topleft_x, box.topleft_y),
                    font,
                    fontScale,
                    fontColor,
                    lineType)

def markPairedBoxes(imgcv, pairs):
    for pair in pairs:
        drawRectangle(pair[0], imgcv, BoxColors.GT_PAIR_COLOR, 3)
        drawRectangle(pair[1], imgcv, BoxColors.PREDICTED_COLOR, 3)


def setColorForClass(label):
    if (label == 'cat'):
        return CAT_COLOR
    elif (label == 'dog'):
        return DOG_COLOR
    elif (label == 'motorbike'):
        return MOTOR_BIKE_COLOR
    elif (label == 'truck'):
        return TRUCK_COLOR
    elif (label == 'bicycle'):
        return BICYCLE_COLOR


def drawFirstPrediction(boxes, img):
    h, w, _ = img.shape
    for b in boxes:
        left = int((b.x - b.w / 2.) * w)
        right = int((b.x + b.w / 2.) * w)
        top = int((b.y - b.h / 2.) * h)
        bot = int((b.y + b.h / 2.) * h)
        cv2.rectangle(img,
                      (left, top),
                      (right, bot),
                      (0, 255, 0),
                      3)
    cv2.imwrite('sample.jpg', img)
