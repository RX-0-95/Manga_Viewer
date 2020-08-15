from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from configparser import ConfigParser
import sys
from os import path

from utilities import Utilities
from toolButton import MangaToolButton


class LineEdit(qtw.QLineEdit):
    
    def __init__(self, contents=None):
        super().__init__(contents)
        self.setReadOnly(True)
        self.returnPressed.connect(self.clear)
        # self.returnPressed.connect(self.clear)

    # if press enter then clear the text and send singal
    def keyPressEvent(self, event):
        self.setReadOnly(False)
        super().keyPressEvent(event)

    def focusOutEvent(self, a0):
        self.setText("To Page")
        self.setReadOnly(True)
        super().focusOutEvent(a0)

    def mouseDoubleClickEvent(self, a0):
        self.clear()
        self.setReadOnly(False)
        return super().mouseDoubleClickEvent(a0)


class PreviewBar(qtw.QWidget):
    def __init__(self):
        super().__init__()
        ##################################
        ###########UI#####################
        ##################################
        
        self.setLayout(qtw.QGridLayout())
        self.go_to_page_edt = LineEdit("To Page")
        self.go_to_page_edt.setAlignment(qtc.Qt.AlignCenter)
        self.go_to_page_edt.setMaximumWidth(70)
        self.go_to_page_edt.setMinimumHeight(40)

        # model-view 
        self.view = qtw.QListView()
        self.model = qtg.QStandardItemModel()
        self.view.setModel(self.model)
        view_style_sheet = """
        QListView
        {
            border: 0px
        }
        """
        self.view.setStyleSheet(view_style_sheet)

        self.bookmark_btn = MangaToolButton(
            Utilities.getBookMarkIconPath(), "Book Marks"
        )

        self.bookmark_btn.setMinimumWidth(70)
        self.bookmark_btn.setMaximumWidth(70)
        self.bookmark_btn.setIconSize(qtc.QSize(30, 30))
        self.add_bookmark_btn = MangaToolButton(
            Utilities.getAddBookMarkIconPath(), "Add \n Book Marks"
        )
        self.add_bookmark_btn.setIconSize(qtc.QSize(30, 30))
        self.add_bookmark_btn.setMinimumWidth(70)
        self.add_bookmark_btn.setMaximumWidth(70)
        left_btn_layout = qtw.QVBoxLayout()
        left_btn_layout.addWidget(self.add_bookmark_btn)
        left_btn_layout.addWidget(self.bookmark_btn)

        # set Layout
        self.layout().setSpacing(0)
        self.layout().setVerticalSpacing(0)
        self.layout().setHorizontalSpacing(0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.go_to_page_edt, 0, 0, 1, 1,qtc.Qt.AlignTop)
        self.layout().addWidget(self.view, 0, 1, 1, 1)
        self.layout().addLayout(left_btn_layout,0,2,1,1,qtc.Qt.AlignTop)


        #############UI END################

    def paintEvent(self, a0):
        opt = qtw.QStyleOption()
        opt.initFrom(self)
        painter = qtg.QPainter(self)
        self.style().drawPrimitive(qtw.QStyle.PE_Widget, opt, painter, self)
        super().paintEvent(a0)


        


if __name__ == "__main__":
    qtw.QApplication.setAttribute(qtc.Qt.AA_EnableHighDpiScaling)
    qtc.QCoreApplication.setAttribute(qtc.Qt.AA_UseHighDpiPixmaps)
    app = qtw.QApplication(sys.argv)
    pb = PreviewBar()
    pb.show()
    sys.exit(app.exec())
