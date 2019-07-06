import os


class FileReader():
    def __init__(self, projectName, fileName, dirName):
        self.__fileName = fileName
        self.__projectName = projectName
        self.__dirName = dirName
        self.__path = self.__createPath()

    def __createPath(self):
        path = './' + self.__dirName + '/' + self.__projectName + '/boxes'
        if (os.path.isdir(path)):
            return path
        else:
            return ''

    def openBoxFile(self):
        filePath = self.__path + '/' + self.__fileName
        if (os.path.isfile(filePath)):
            return open(filePath, 'r+')

    def openTimeFile(self):
        filePath = './' +self.__dirName + '/' + self.__projectName +'/time/time.json'
        if (os.path.isfile(filePath)):
            return open(filePath, 'r+')
