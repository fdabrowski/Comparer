import argparse

from src.file_readers.XmlReader import XmlReader

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("project_name", help="Set project name.", type=str)
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parseArguments()
    project_name = args.__dict__['project_name']
    xml_reader = XmlReader(project_name)
    xml_reader.convert_xml_to_txt()