from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

class MangaToolButton(qtw.QToolButton):
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

    #def sizeHint(self):
    #    _screen = self.screen()
    #    screen_height = _screen.geometry().height()
    #    return qtc.QSize(super().sizeHint().width(), int(screen_height / 18))