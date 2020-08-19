from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import sys
from os import path
from utilities import Utilities
from utilities import MangaLayout
from zipBookReader import BookCoverLoader
#from magaViewer.utilities import MangaLayout
#####LALALALA################################

class ViewToolBar(qtw.QWidget):
    layout_change = qtc.pyqtSignal(MangaLayout)
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.__buttons = []
        self.setLayout(qtw.QGridLayout())
        self.book_shelf_btn = ViewToolButton(
            Utilities.getBookShelfIconPath(), "Book Shelf"
        )

        self.setting_btn = ViewToolButton(Utilities.getSettingIconPath(), "Settings")
        self.info_btn = ViewToolButton(Utilities.getInfoIconPath(), "Info")
        self.layout().setSpacing(0)
        self.layout().setVerticalSpacing(0)
        self.layout().setHorizontalSpacing(0)
        self.layout().addWidget(self.book_shelf_btn, 0, 0, 1, 1, qtc.Qt.AlignAbsolute)
        self.layout().addWidget(self.setting_btn, 0, 1, 1, 1)
        self.layout().addWidget(self.info_btn, 0, 2, 1, 1)

        self.label = qtw.QLineEdit()
        self.label.setText("fdsafdsafdsafdsafdsafdsafdsaffdsafdsafdsafdsafdsafdsafdsa")
        self.layout().addWidget(self.label, 0, 3, 1, 1)
        self.label.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Minimum)
        self.label.setContentsMargins(0, 0, 0, 0)

        self.book_shelf_btn4 = ViewToolButton(
            Utilities.getPageLayoutIconPath(), "Page Layout"
        )
        self.prev_btn = ViewToolButton(Utilities.getPrevIconPath(), "Prev Book")
        self.next_btn = ViewToolButton(Utilities.getNextIconPath(), "Next Book")
        self.__buttons.append(self.book_shelf_btn)
        self.__buttons.append(self.setting_btn)
        self.__buttons.append(self.info_btn)
        self.__buttons.append(self.book_shelf_btn4)
        self.__buttons.append(self.prev_btn)
        self.__buttons.append(self.next_btn)
        icon_size = int(30)
        for button in self.__buttons:
            button.setIconSize(qtc.QSize(icon_size, icon_size))

        self.layout().addWidget(self.book_shelf_btn4, 0, 4, 1, 1)
        self.layout().addWidget(self.prev_btn, 0, 5, 1, 1)
        self.layout().addWidget(self.next_btn, 0, 6, 1, 1)

        self.layout().setContentsMargins(0, 0, 0, 0)

    #Setting allow this widget able to use style sheet 
    def paintEvent(self, a0):
        opt = qtw.QStyleOption()
        opt.initFrom(self)
        painter = qtg.QPainter(self)
        self.style().drawPrimitive(qtw.QStyle.PE_Widget, opt, painter, self)
        super().paintEvent(a0)

    def wheelEvent(self, a0):
        print("View Tool Bar Wheel Event")
        return super().wheelEvent(a0)
    
    def openPageLayoutToolBar(self):
        None

#######TO DO: change the color of the icon based on style
class ViewToolButton(qtw.QToolButton):
    changed = qtc.pyqtSignal()

    def __init__(self, icon_path=None, text=None, changed=None):
        super().__init__()
        # self.setStyleSheet("background-color: rgba(0,0,0,0); color: white;")
        styleSheet = """
        ViewToolButton
        {
            background-color: rgba(0,0,0,0); 
            color: white;
        }
        ViewToolButton:hover
        {
            background-color: rgba(0,0,0,185);   
        }
        """
        self.on_widget = None
        # self.setStyleSheet(styleSheet)
        self.setToolButtonStyle(qtc.Qt.ToolButtonTextUnderIcon)
        self.clicked.connect(self.on_click)
        if icon_path:
            self.setIcon(qtg.QIcon(icon_path))
        if text:
            self.setText(text)
        if changed:
            self.changed.connect(changed)
        # self.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)

    def setOnWidget(self, widget):
        self.on_widget = widget

    def on_click(self):
        self.changed.emit()

    def wheelEvent(self, a0):
        print("Tool Button Wheel event")
        return super().wheelEvent(a0)

class pageLayoutToolBar(qtw.QToolBar):
    def __init__(self, title=None, parent=None):
        super().__init__(title, parent)