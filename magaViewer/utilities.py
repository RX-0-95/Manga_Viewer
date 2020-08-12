from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import sys
from os import path

class Utilities():
    
    def getDefaultCoverPath():
        return Utilities.getImagePath('book_loading.jpg')

    def getWinOpenFolderPath():
        return Utilities.getImagePath("Win_open_folder.png")

    def getImagePath(file_name):
        directory = path.dirname(__file__)
        file_path = path.join(directory, 'images', file_name)
        file_path = str(file_path)
        return file_path


if __name__ == "__main__":
    #base_name = path.basename(Utilities.getDefaultCoverPath())
    base_name = Utilities.getWinOpenFolderPath()
    print(base_name)