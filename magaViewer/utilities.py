from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import sys
from os import path

class Utilities():
    
    def CurrentDir():
        directory = None
        if getattr(sys, "frozen", False):
            directory = sys._MEIPASS
        else:  # Not frozen
            directory = path.dirname(__file__)
        return directory

    def getImagePath(file_name):
        directory = None
        if getattr(sys, "frozen", False):
            directory = sys._MEIPASS
        else:  # Not frozen
            directory = path.dirname(__file__)
        file_path = path.join(directory, 'images', file_name)
        file_path = str(file_path)
        return file_path
        
    def getDefaultCoverPath():
        return Utilities.getImagePath('book_loading.jpg')

    def getWinOpenFolderPath():
        return Utilities.getImagePath("Win_open_folder.png")   
    @staticmethod
    def getBookShelfIconPath():
        return Utilities.getImagePath("book_shelf_icon.png")

    def getSettingIconPath():
        return Utilities.getImagePath("setting_icon.png")
    
    def getInfoIconPath():
        return Utilities.getImagePath("Win10_info_icon.png")

    def getNextIconPath():
        return Utilities.getImagePath("next_icon.png")
    def getPrevIconPath():
        return Utilities.getImagePath("previous_icon.png")

    def getBookMarkIconPath():
        return Utilities.getImagePath("book_mark_icon.png")

    def getAddBookMarkIconPath():
        return Utilities.getImagePath("add_bookmark_icon.png")
    @staticmethod
    def getSettingFilePath():
        return path.join(Utilities.CurrentDir(),"setting.ini")
    
    
   


if __name__ == "__main__":
    #base_name = path.basename(Utilities.getDefaultCoverPath())
    base_name = Utilities.getSettingFilePath()
    print(base_name)