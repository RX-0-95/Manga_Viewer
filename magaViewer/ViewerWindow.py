from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import sys
from os import path
from utilities import Utilities
from zipBookReader import BookCoverLoader
from dev_tool import DebugWindow
from previewBar import PreviewBar
from fileMatch import FileMatch as fm
import zipfile


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

    def wheelEvent(self, a0):
        print("View Tool Bar Wheel Event")
        return super().wheelEvent(a0)


###############################
#########Book Object###########
###############################
# Send a signal of QPixmap
# page num start at 0
class AbstractBookObj(qtc.QObject):
    ##Signal
    page_changed = qtc.pyqtSignal(int)
    page_count_changed = qtc.pyqtSignal(int)
    page_start_reached = qtc.pyqtSignal()
    page_end_reached = qtc.pyqtSignal()
    pixmap_sgn = qtc.pyqtSignal(qtg.QPixmap)

    def __init__(self, path=None):
        super().__init__()
        self.current_page = 1
        self.path = path
        self.page_count = 0
        self.page_count_changed.connect(self.setPageCount)
        self.current_pixmap = None
        self.pixmap_sgn.connect(self.setPixmap)

    # Pure Virtual function need override, on need
    # to worry about page out of bound, Must emit
    # QPixmap of the current page
    def openPage(self, page_num):
        raise NotImplementedError()

    # Must implement pageCount function, must emit the
    # page count chagned signal with page count
    def updatePageCount(self):
        raise NotImplementedError()

    # Regual method
    @qtc.pyqtSlot(qtg.QPixmap)
    def setPixmap(self, pixmap):
        self.current_pixmap = pixmap

    @qtc.pyqtSlot(int)
    def setPageCount(self, count):
        self.page_count = count

    #####TO DO: finished setPath: re init book object
    def setPath(self, path):
        self.path = path
        self.updatePageCount()
        self.current_page = 1

    @qtc.pyqtSlot(int)
    def goToPage(self, page_num):
        if page_num < 1:
            self.page_start_reached.emit()
            return
        if page_num == self.page_count:
            self.page_end_reached.emit()
            return
        self.current_page = page_num
        print(f"Currnet page: {page_num}")
        # emit the page num
        self.page_changed.emit(page_num)
        # Check if the page out of bound
        self.openPage(self.current_page)

    def nextPage(self):
        self.goToPage(self.current_page + 1)

    def prevPage(self):
        self.goToPage(self.current_page - 1)


######Zip Book object##########
class ZipBookObj(AbstractBookObj):
    def __init__(self, path):
        super().__init__(path)
        self.zip_file = None
        try:
            self.zip_file = zipfile.ZipFile(path)
        except Exception as e:
            qtw.QMessageBox.information(None, "Fail to open zip file", str(path))
        self.imageFileList = []
        self.updatePageCount()

    def __del__(self):
        print("deleting zipBookObject")
        if self.zip_file:
            self.zip_file.close()

    def updatePageCount(self):
        if not self.zip_file:
            return
        file_list = self.zip_file.namelist()
        page_count = -1
        for filename in file_list:
            # print(f"filename: {filename}")
            if fm.isImage(filename):
                self.imageFileList.append(filename)
                page_count += 1
        self.page_count_changed.emit(page_count)

    def openPage(self, page_num):
        # print(f"Opening Image: {page_num}")
        pixmap = qtg.QPixmap()
        pixmap.loadFromData(self.zip_file.open(self.imageFileList[page_num]).read())
        # print(f"emit pixmap: {pixmap}")
        self.pixmap_sgn.emit(pixmap)
        return pixmap


#######Dir Book Object#########
class DirBookObj(AbstractBookObj):
    def __init__(self):
        super().__init__()


#################################
###Custom QGraphicScence/view####
#################################
class BookScene(qtw.QGraphicsScene):
    book_changed = qtc.pyqtSignal()
    reach_scene_bottom = qtc.pyqtSignal()
    reach_scene_top = qtc.pyqtSignal()

    def __init__(self, file_path=None, parent=None):
        super().__init__(parent)
        self.currentPixmap = qtw.QGraphicsPixmapItem()
        self.addItem(self.currentPixmap)
        self.installEventFilter(self)
        self.book = None
        if file_path:
            self.initBook(file_path)

    # init of the book, include connection to the scene
    def initBook(self, file_path):
        # when zip/dir file
        if fm.isZip(str(file_path)):
            self.book = ZipBookObj(file_path)
        elif path.isdir(str(file_path)):
            self.book = DirBookObj(file_path)
        if not self.book:
            qtw.QMessageBox.critical(None, "Can't open Book", str(file_path))
            return
        self.book.pixmap_sgn.connect(self.setPixmap)
        self.book.goToPage(190)
        self.book_changed.emit()
    
    def nextPage(self):
        if self.book:
            self.book.nextPage()
    
    def prevPage(self):
        if self.book:
            self.book.prevPage()
    
    def goToPage(self,num):
        if self.book:
            self.book.goToPage(num)

    def eventFilter(self, watched, event):
        # handle QEvent.Wheel
        if event.type() == qtc.QEvent.Wheel:
            print("catche wheel event in Book scene")
            # emit the signal based on the direction of the wheel
            if event.angleDelta().y() > 0:
                self.reach_scene_top.emit()
            elif event.angleDelta().y() < 0:
                self.reach_scene_bottom.emit()
            return True
        return super().eventFilter(watched, event)

    def wheelEvent(self, event):
        if event.type() == qtc.QEvent.Wheel:
            print("Scene Wheel Event--------------------------------")
            print("wheel inside Scene")
        if event.type() == qtc.QEvent.GraphicsSceneWheel:
            print("GraphicsSceneWheel")

        super().wheelEvent(event)
        # print(f"Scene Wheel: {event.delta()}")
        # print(f"Scene Wheel scene pos: {event.scenePos()}")
        # print(f"Scene Wheel screen pos: {event.screenPos()}")

    @qtc.pyqtSlot(qtg.QPixmap)
    def setPixmap(self, pixmap):
        self.currentPixmap.setPixmap(pixmap)
        # self.currentPixmap.moveBy(1000,100)
        print(f"pixmap size: {pixmap.size().width(), pixmap.size().height()}")
        self.update()

    def update(self):
        print(f"scene Rect: {self.sceneRect()}")
        return super().update()


class BookView(qtw.QGraphicsView):
    wheel_up = qtc.pyqtSignal()
    wheel_down = qtc.pyqtSignal()

    def __init__(self, scene=None, parent=None):
        super().__init__(scene, parent)
        if self.scene():
            self.connectUI()

    def setScene(self, scene):
        super().setScene(scene)    
        self.connectUI()
        

    # Reimplement the wheel event, the original version has a bug of triggered twice
    # When scroll to bottom, eat the event and send another one to mainwindow

    def wheelEvent(self, event):
        #########TO DO: Add support of horizontal wheel option
        # print(f"Margines: {self.viewportMargins().left(), self.viewportMargins().top(),self.viewportMargins().right(),self.viewportMargins().bottom()}")
        print(f"Scene Rect: {self.sceneRect()}")
        print(f"View Rect: {self.viewport().geometry()}")
        # View Rect's topLeft somehow start at (1,1), translate to origin (0,0)
        view_rect_ori = self.viewport().geometry()
        view_rect_ori.translate(-view_rect_ori.topLeft())
        view_rect_mapped = self.mapToScene(view_rect_ori).boundingRect()
        print(f"View Rect after map: {view_rect_mapped}")
        print(f"view map to scene bottom right : {view_rect_mapped.bottomRight()}")
        print(f"view map to scene top left : {view_rect_mapped.topLeft()}")
        # When the view scroll to the end of the scene, eat the event and send event to scene
        # When the view scroll to the top of the scene eat the event and send even to scene
        scene_rect = self.sceneRect()
        if (
            scene_rect.bottomRight().y() <= view_rect_mapped.bottomRight().y()
            and event.angleDelta().y() < 0
        ) or (
            scene_rect.topLeft().y() >= view_rect_mapped.topLeft().y()
            and event.angleDelta().y() > 0
        ):
            print("Send evnet to scene**********************")
            if self.scene():
                qtw.QApplication.sendEvent(self.scene(), event)
            event.accept()
            return
        # elif (scene_rect.topLeft().y() >= view_rect.topLeft().y() and
        #    event.angleDelta().y()>0):

        #    print("Send evnet to scene**********************")
        #    qtw.QApplication.sendEvent(self.scene(),event)
        #    event.accept()
        #   return

        super().wheelEvent(event)

        # self.scene().wheelEvent(event)

    ####ConnectUI is connect to the bookchanged signal of the graphics scene
    def connectUI(self):
        #####Connect book with Action######
        self.next_page_action = qtw.QAction("next page")
        self.addAction(self.next_page_action)
        self.prev_page_action = qtw.QAction("prev page")
        self.addAction(self.prev_page_action)
        ###########Connect to UI#############################
        # self.book.pixmap_sgn.connect(self.updateImage)
        self.next_page_action.triggered.connect(self.scene().nextPage)
        self.prev_page_action.triggered.connect(self.scene().prevPage)
        self.scene().reach_scene_bottom.connect(self.nextPage)
        self.scene().reach_scene_top.connect(self.prevPage)
        #########Shortcuts for Action##############################
        short_cuts = []
        short_cuts.append(qtc.Qt.Key_Plus)
        short_cuts.append(qtc.Qt.Key_Equal)
        self.next_page_action.setShortcuts(short_cuts)
        short_cuts.clear()
        short_cuts.extend([qtc.Qt.Key_Minus, qtc.Qt.Key_hyphen])
        self.prev_page_action.setShortcuts(short_cuts)

    def nextPage(self):
        self.scene().nextPage()
        self.verticalScrollBar().setValue(0)
    
    def prevPage(self):
        self.scene().prevPage()
        self.verticalScrollBar().setValue(0)

class ViewerWindow(qtw.QMainWindow):
    def __init__(self, book_shelf=None):
        super().__init__()
        self.resize(1000, 800)
        self.initUI()
        # self.setStyleSheet("background-color: 'black")
        self.connectUI()

        self.book_shelf = book_shelf
        self.book_path = None
        self.current_page = 1

        # self.setMouseTracking(True)
        ###################
        ###BOOK OBJ #######
        ###################

        # self.book = ZipBookObj("resource/test_zip_file.zip")
        # print(f"page Count: {self.book.page_count}")
        # self.book.pixmap_sgn.connect(self.updateImage)

        #######################################
        self.graphics_scene.initBook("resource/test_zip_file.zip")
        self.graphics_scene.initBook("resource/test_zip_file.zip")
        #self.initBook("resource/test_zip_file.zip")

        # self.graphics_scene.installEventFilter(self)
        #self.installEventFilter(self)
        # self.graphics_view.installEventFilter(self)
        # self.graphics_view.scene().installEventFilter(self)
        # self.graphics_view.installEventFilter(self)
        # self.installEventFilter(self)
        ##########################################################
        self.show()

        ####TO DO: wheel event call twice

    def wheelEvent(self, wheelEvent):
        # print(f"whell:{wheelEvent.angleDelta()} ")
        print(f"source: {wheelEvent.source()}")
        if wheelEvent.angleDelta().y() > 0:
            print("up")
            self.book.prevPage()
        else:
            print("down")
            self.book.nextPage()

        # return super().wheelEvent(wheelEvent)

    def eventFilter(self, QObject, QEvent):
        # print(QEvent.type())
        # print(f"sender: {QEvent.sender()}")

        if QEvent.type() == qtc.QEvent.GraphicsSceneWheel:
            print(f"{QObject}: graphicsScene view wheel")
            # QEvent.ignore()
            # self.graphics_view.scene().wheelEvent(QEvent)
            # return True
        if QEvent.type() == qtc.QEvent.Wheel:
            # print(self)
            print(f"{QObject}: kill wheel from graphics_scene")
            if QObject == self.graphics_scene:
                self.wheelEvent(QEvent)
                QEvent.accept()
                return True

        return False

    # use layout on this one
    def initUI(self):
        self.setWindowTitle("Manga Viewer")
        # Add Image View section use Qgraphics view and scence
        self.main_widget = qtw.QWidget(self)
        self.main_layout = qtw.QGridLayout(self)
        self.main_layout.setSpacing(0)
        self.graphics_scene = BookScene(parent = self)
        self.graphics_view = BookView(self.graphics_scene)
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

    def initBook(self, file_path):
        # when zip/dir file
        if fm.isZip(str(file_path)):
            self.book = ZipBookObj(file_path)
        elif path.isdir(str(file_path)):
            self.book = DirBookObj(file_path)
        if not self.book:
            qtw.QMessageBox.critical(self, "Can't open Book", str(file_path))
            return
        # self.book.pixmap_sgn.connect(self.updateImage)
        self.book.pixmap_sgn.connect(self.graphics_scene.setPixmap)
        self.book.goToPage(10)
        #####Connect book with Action
        self.next_page_action = qtw.QAction("next page")
        self.addAction(self.next_page_action)
        self.prev_page_action = qtw.QAction("prev page")
        self.next_page_action.triggered.connect(self.book.nextPage)
        self.prev_page_action.triggered.connect(self.book.nextPage)
        short_cuts = []
        short_cuts.append(qtc.Qt.Key_Plus)
        self.next_page_action.setShortcuts(short_cuts)

    def setBookShelf(self, book_shelf):
        self.book_shelf = book_shelf

    # Open zip book or dir book
    ###TO DO: add support of RAR file, 7zip file so no

    def setBookPathAndOpen(self, book_path):
        self.book_path = book_path
        self.openBook()

    def connectUI(self):
        # self.book.pixmap_sgn.connect()
        None

    @qtc.pyqtSlot(qtg.QPixmap)
    def updateImage(self, pixmap):
        # print("show Image ")
        # print(f"pixmap: {pixmap}")
        self.graphics_scene.clear()
        # self.graphics_view.resetMatrix()
        self.graphics_scene.addPixmap(pixmap)
        self.graphics_scene.update()
        self.graphics_view.setSceneRect(qtc.QRectF(pixmap.rect()))

    #######Mosue and Wheel Event
    def mousePressEvent(self, mouseEvent):
        print(mouseEvent.button())
        if mouseEvent.button() == qtc.Qt.RightButton:
            self.toogleBar()
        super().mousePressEvent(mouseEvent)

    def mouseMoveEvent(self, event):
        print("move")
        super().mouseMoveEvent(event)

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
