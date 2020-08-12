
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import sys
from os import path

from zipBookReader import BookCoverLoader
from dev_tool import DebugWindow


class PreviewBar(qtw.QWidget):
    def __init__(self, parent, flags):
        super().__init__(parent, flags)



class ViewerWindow(qtw.QMainWindow):

    def __init__(self):
        super().__init__()


    #use layout on this one 
    def initUI(self):
        None






if __name__ == "__main__":
    
    app = qtw.QApplication(sys.argv)
    mw = ViewerWindow()

    sys.exit(app.exec())
