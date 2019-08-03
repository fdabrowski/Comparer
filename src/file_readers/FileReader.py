import os


class FileReader():
    def __init__(self, project_name, video_name, file_name, dir_name):
        self.__file_name = file_name
        self.__project_name = project_name
        self.__video_name = video_name
        self.__dir_name = dir_name
        self.__path = self.__create_path()

    def __create_path(self):
        path = './' + self.__dir_name + '/' + self.__project_name + '/' + self.__video_name + '/boxes'
        if (os.path.isdir(path)):
            return path
        else:
            return ''

    def open_box_file(self):
        filePath = self.__path + '/' + self.__file_name
        if (os.path.isfile(filePath)):
            return open(filePath, 'r+')

    def open_time_file(self):
        filePath = './' + self.__dir_name + '/' + self.__project_name + '/' + self.__video_name + '/time/time.json'
        if (os.path.isfile(filePath)):
            return open(filePath, 'r+')
