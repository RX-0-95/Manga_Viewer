from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from configparser import ConfigParser
import sys
from os import path

from utilities import Utilities


class PreviewBar(qtw.QWidget):
    def __init__(self):
        super().__init__()
        ##################################
        ###########UI#####################
        ##################################
        self.resize(1000,900)
        self.setLayout(qtw.QVBoxLayout())
        
        

        #############UI END################
        self.show()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    pb = PreviewBar()
    sys.exit(app.exec())
