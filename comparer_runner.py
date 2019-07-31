import argparse
import os
from label_source import LabelSource


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("video_path", help="Set video path.", type=str)
    parser.add_argument("label_source", help="Set label source.", type=str)
    args = parser.parse_args()
    return args

def createModifiedVideos():
    os.system("python3 video_creator.py " + project_name + " dark")
    os.system("python3 video_creator.py " + project_name + " light")
    os.system("python3 video_creator.py " + project_name + " blur")

if __name__ == "__main__":
    args = parseArguments()
    video_name = args.__dict__['video_path']
    label_source = LabelSource[args.__dict__['label_source']]
    project_name, format = video_name.split('.')

    createModifiedVideos()


    print(video_name)
    print(label_source)
    print(project_name)

