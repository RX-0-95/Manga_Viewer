from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import sys
from os import path
from utilities import Utilities
from zipBookReader import BookCoverLoader
from dev_tool import DebugWindow
from previewBar import PreviewBar


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


class ViewToolBar(qtw.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.setStyleSheet("background-color:black")
        # self.setAttribute(qtc.Qt.WA_TranslucentBackground,True)
        # self.setStyleSheet("background-color: rgba(0,0,0,128)")

        style_sheet = """
        ViewToolBar
        {
            background-color: rgba(0,0,0,128);
        }
        ViewToolButton
        {
            background-color: rgba(0,0,0,0); 
            color: white;
        }
        ViewToolButton:hover
        {
            background-color: rgba(0,0,0,185);   
        }
        QLineEdit
        {
            background: rgba(0,0,0,0);   
            border: 0px
        }
        QTextEdit
        {
            background: rgba(0,0,0,0);   
            border: 0px
        }
        """
        # self.setStyleSheet(style_sheet)
        # self.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        # self.setSizePolicy(qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Minimum)
        # layout
        # main_widget = qtw.QWidget()
        # main_widget.setStyleSheet("background-color: red")
        # main_layout = qtw.QGridLayout()
        # main_widget.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
        # Book shelf Button
        # use to hold all buttons for resize when print
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
            Utilities.getBookShelfIconPath(), "Book Shelf4"
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

        # self.view_label = qtw.QLabel()
        # self.view_label.setSizePolicy(qtw.QSizePolicy.Minimum, qtw.QSizePolicy.Maximum)
        # self.addWidget(self.view_label)

        # book_shelf_btn_icon = qtg.QIcon(
        #    qtg.QPixmap(Utilities.getBookShelfIconPath()))
        # self.book_shelf_act = qtw.QAction(book_shelf_btn_icon,
        #    "Book Shelf")
        # self.addAction(self.book_shelf_act)
        # main_widget.setLayout(main_layout)
        # main_widget.layout().setContentsMargins(0, 0, 0, 0)
        # self.addWidget(main_widget)

    # def sizeHint(self):
    #
    #    print("hint")
    #    _screen = self.screen()
    #    screen_height = _screen.geometry().height()
    #    icon_size = int(screen_height*60/2048)
    #    return qtc.QSize(super().sizeHint().width(), int(screen_height / 18))

    def paintEvent(self, a0):
        opt = qtw.QStyleOption()
        opt.initFrom(self)
        painter = qtg.QPainter(self)
        self.style().drawPrimitive(qtw.QStyle.PE_Widget, opt, painter, self)
        super().paintEvent(a0)


class ViewerWindow(qtw.QMainWindow):
    def __init__(self, book_shelf=None):
        super().__init__()
        self.resize(1000, 800)
        self.initUI()
        # self.setStyleSheet("background-color: 'black")
        self.connectUI()

        self.book_shelf = book_shelf
        self.book_path = None
        self.show()

    # use layout on this one
    def initUI(self):
        self.setWindowTitle("Manga Viewer")
        # Add Image View section use Qgraphics view and scence
        self.main_widget = qtw.QWidget(self)
        self.main_layout = qtw.QGridLayout()
        self.main_layout.setSpacing(0)
        graphics_scence = qtw.QGraphicsScene(self)
        self.graphics_view = qtw.QGraphicsView(graphics_scence)
        self.menu_bar = ViewToolBar()
        # Set up the preview Bar
        self.preview_bar = PreviewBar()

        # set layout
        self.main_layout.addWidget(self.graphics_view, 0, 0, 18, 1)
        self.main_layout.addWidget(self.menu_bar, 0, 0, 1, 1)
        self.main_layout.addWidget(self.preview_bar, 14, 0, 4, 1)

        self.main_widget.setLayout(self.main_layout)
        self.main_widget.layout().setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.main_widget)

        ###########set style#######################

        style_sheet = """
        ViewToolBar
        {
            background-color: rgba(0,0,0,128);
        }
        ViewToolButton
        {
            background-color: rgba(0,0,0,0); 
            color: white;
        }
        ViewToolButton:hover
        {
            background-color: rgba(0,0,0,185);   
        }
        QToolButton
        {
            background-color: rgba(0,0,0,0); 
            color: white;
        }
        QToolButton:hover
        {
            background-color: rgba(0,0,0,185);   
        }
        QLineEdit
        {
            background-color: rgba(0,0,0,0); 
            color: white;  
            border: 0px;
            section-background-color: darkgray;
            font-size: 15px;
        }
        QLineEdit:focus
        {
            background-color: rgba(0,0,0,60); 
        }
        PreviewBar
        {
        
            background-color: rgba(0,0,0,128);
        }
        QListView
        {
            background-color: rgba(0,0,0,60);
        }
        QGraphicsView
        {
             background-color: rgba(0,0,0,50);
        }
        """
        self.setStyleSheet(style_sheet)

    def setBookPath(self, path):
        self.book_path = path

    #Open zip book or dir book
    def openBook(self):
        #detect the 
        None


    def connectUI(self):
        None



    def mousePressEvent(self, mouseEvent):
        if mouseEvent.button() == qtc.Qt.RightButton:
            self.toogleBar()
        super().mousePressEvent(mouseEvent)

    def toogleBar(self):
        if self.menu_bar.isVisible():
            self.menu_bar.setVisible(False)
            self.preview_bar.setVisible(False)
        else:
            self.menu_bar.setVisible(True)
            self.preview_bar.setVisible(True)

    # Press Bookshelf button and back to book shelf, set the current Bookshelf to
    def goToBookShelf(self):
        None


if __name__ == "__main__":
    qtw.QApplication.setAttribute(qtc.Qt.AA_EnableHighDpiScaling)
    qtc.QCoreApplication.setAttribute(qtc.Qt.AA_UseHighDpiPixmaps)
    # QGuiApplication::setHighDpiScaleFactorRoundingPolicy(Qt::HighDpiScaleFactorRoundingPolicy::RoundPreferFloor)
    qtw.QApplication.setHighDpiScaleFactorRoundingPolicy(
        qtc.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = qtw.QApplication(sys.argv)

    mw = ViewerWindow()
    # kw = ViewerWindow()
    # setAttribute(qtc.Qt.WA_StyledBackground, True)
    sys.exit(app.exec())
