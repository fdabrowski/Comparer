from xml.dom import minidom


class XmlReader:
    path = 'samples/xml_boxes/'
    xml_tag = 'track'
    def __init__(self, fileName) -> None:
        self.file_name = fileName
        self.out_path = XmlReader.path + self.file_name + '/boxes'

    def __open_box_file(self):
        filePath = XmlReader.path + self.file_name
        if (os.path.isfile(filePath)):
            return open(filePath, 'r+')

    def __open_xml_file(self):
        return minidom.parse(XmlReader.path + self.file_name)

    def __filter_all_track_objects(self, file):
        return file.getElementsByTagName(XmlReader.xml_tag)

    def __save_objects_to_files(self, track_objects):
        for object in track_objects:
            frame_file = open(self.out_path, 'r+')
            frame_file

    def convert_xml_to_txt(self):
        file = self.__open_xml_file()
        track_objects = self.__filter_all_track_objects(file)
        self.__save_objects_to_files(track_objects)
