import os
from typing import List
from xml.dom import minidom
from xml.dom.minicompat import NodeList

from src.model.BoundingBox import BoundingBox


class XmlReader:
    path = 'samples/xml_boxes/'
    truck_tag = 'track'
    box_tag = 'box'
    label_tag = 'label'
    frame_tag = 'frame'
    def __init__(self, fileName) -> None:
        self.file_name = fileName
        self.out_path = XmlReader.path + self.file_name + '/boxes'

    def __open_box_file(self):
        filePath = XmlReader.path + self.file_name
        if (os.path.isfile(filePath)):
            return open(filePath, 'r+')

    def __open_xml_file(self):
        return minidom.parse(XmlReader.path + self.file_name + '/' + self.file_name + '.xml')

    def __filter_all_track_objects(self, file):
        return file.getElementsByTagName(XmlReader.truck_tag)

    def __create_bouding_box_from_tag(self, box, label):
        return BoundingBox(
            box.getElementsByTagName('xtl'),
            box.getElementsByTagName('ytl'),
            box.getElementsByTagName('xbr'),
            box.getElementsByTagName('ybr'),
            label
        )

    def __save_txt(self, frame_file, bounding_box_list: List[BoundingBox]):
        for bounding_box in bounding_box_list:
            gt_values = str(bounding_box.downright_x) + ' ' + str(bounding_box.downright_y) + ' ' + str(
                bounding_box.topleft_x) + ' ' + str(bounding_box.topleft_y) + ' ' + bounding_box.object_class + '\n'
            frame_file.write(gt_values)


    def __save_objects_to_files(self, track_objects: NodeList, frames_number: int):
        for number in range(0, frames_number):
            frame_file = open(self.out_path + '/frame' + str(number) + '.txt', 'w+')
            bounding_boxes = []
            for object in track_objects:
                label = object.getElementsByTagName(XmlReader.label_tag)
                boxes = self.__get_boxes(object)
                for box in boxes:
                    frame_number = box.getElementsByTagName(XmlReader.frame_tag)
                    if number == frame_number:
                        bounding_boxes.append(self.__create_bouding_box_from_tag(box, label))
            self.__save_txt(frame_file, boxes)


    def __get_frames_number(self, xml_file) -> int:
        all_boxes = self.__get_boxes(xml_file)
        frames_number = 0
        for box in all_boxes:
            box_frame = int(box.attributes[XmlReader.frame_tag].value)
            if box_frame > frames_number:
                frames_number = box_frame
        return frames_number


    def __get_boxes(self, xml_file):
        return xml_file.getElementsByTagName(XmlReader.box_tag)

    def convert_xml_to_txt(self):
        xml_file = self.__open_xml_file()
        frames_number = self.__get_frames_number(xml_file)
        track_objects = self.__filter_all_track_objects(xml_file)
        self.__save_objects_to_files(track_objects, frames_number)
