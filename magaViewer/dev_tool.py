
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from configparser import ConfigParser
import sys
from os import path






class DebugWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1000,800)
        
    def printIcon(self, icon):
        pixmap = icon.pixmap(50,50)
        self.printPixmap(pixmap)

    def printPixmap(self, pixmap):
        self.graphicsScence = qtw.QGraphicsScene()
        self.graphicsScence.clear()
        self.graphicsScence.addPixmap(pixmap)
        self.graphicsView = qtw.QGraphicsView()
        self.graphicsView.setScene(self.graphicsScence)
        self.graphicsScence.update()
        self.setCentralWidget(self.graphicsView)


if __name__ == "__main__":

    app = qtw.QApplication(sys.argv)
    mw = DebugWindow()

    sys.exit(app.exec())

    
   