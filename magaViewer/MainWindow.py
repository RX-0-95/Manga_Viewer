from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from configparser import ConfigParser
import sys
from os import path

from zipBookReader import BookCoverLoader
from dev_tool import DebugWindow
from bookShelf import BookShelf
from utilities import Utilities


SETTING_FILE = "setting.ini"
SETTING_SECTION_PATHS = "Paths"


class SideBar(qtw.QToolBar):
    def __init__(self):
        super().__init__()

        self.show()


class MainWindow(qtw.QMainWindow):
    # signal
    open_file_path = qtc.pyqtSignal(str)

    def __init__(self):
        super().__init__()

        ############
        ##Config####
        ############
        #self._config = ConfigParser()
        # get the path based on executable or python file
        #directory = None
        #if getattr(sys, "frozen", False):
        #    directory = sys._MEIPASS
        #else:  # Not frozen
        #    directory = path.dirname(__file__)
        #self._setting_file_path = path.join(directory, SETTING_FILE)

        #self._config.read(self._setting_file_path)
        self.setting_path = Utilities.getSettingFilePath()
        setting = qtc.QSettings(self.setting_path, qtc.QSettings.IniFormat)
        # init the image folder path
        if setting.value("User_settings/book_folder"):
            self.book_folder_path = setting.value("User_settings/book_folder")
        else:
            self.book_folder_path = qtc.QDir.homePath()
            setting.setValue("User_settings/book_folder", self.book_folder_path)


        #try:
        #    self._image_folder_path = self._config[SETTING_SECTION_PATHS][
        #        "open_file_path"
        #    ]
        #    # print(self._config[SETTING_SECTION_PATHS]['open_file_path'])
        #    # print(self._open_file_path)
        #except:
        #    self._image_folder_path = qtc.QDir.homePath()

        #self._qsetting_file_path = str(path.join(directory, "qsetting.ini"))

        # print(qsetting_file_path)
        # self._qsetting = qtc.QSettings(qsetting_file_path, qtc.QSettings.IniFormat)
        # self._qsetting.setValue("1", 'fdsf')

        # MAIN UI Start
        self.initUI()
        # Main UI End

        self.show()

    def initUI(self):
        ################
        #####SET UI#####
        ################
        self.setWindowTitle("Manga Viwer")
        # Open Setting file
        qsetting = qtc.QSettings(self.setting_path, qtc.QSettings.IniFormat)
        # Restore the size and the position of the mainwindow
        if qsetting.value("MainWindow/geometry"):
            self.restoreGeometry(qsetting.value("MainWindow/geometry"))
        else:
            self.resize(1000, 800)

        if qsetting.value("MainWindow/windowState"):
            self.restoreState(qsetting.value("MainWindow/windowState"))


        ###Status Bar####
        self._main_status_bar = qtw.QStatusBar()
        self._status_label = qtw.QLabel()
        self._file_count_label = qtw.QLabel()
        self._file_count_label.setAlignment(qtc.Qt.AlignCenter)
        self._main_status_bar.addPermanentWidget(self._status_label)
        self._main_status_bar.addWidget(self._file_count_label)
        self.setStatusBar(self._main_status_bar)
        self._status_label.setText(str(self.book_folder_path))
        ###################
        #####Book Shelf####
        ###################

        self.book_shelf = BookShelf()
        self.setCentralWidget(self.book_shelf)
        ###############Connect book shelf to UI################
        self.open_file_path.connect(self.book_shelf.loadBooks)
        self.book_shelf.getView().doubleClicked.connect(self.book_shelf.updateBookProgressFromIndex)
        self.book_shelf.getView().doubleClicked.connect(self.book_shelf.updateCover)
        self.book_shelf.getModel().file_count_sgn.connect(
            lambda x,y: self._file_count_label.setText(f"        {x} Books, {y} Folders"))
        
        ##############Connect END##############################

        ###################
        #####TOOL BAR######
        ###################
        self.main_toolbar = qtw.QToolBar("Side_Bar")
        self.addToolBar(qtc.Qt.LeftToolBarArea, self.main_toolbar)
        self.main_toolbar.setMovable(False)
        # Open Folder Action
        dirrectory = path.dirname(__file__)

        # open_folder_icon = qtg.QIcon(path.join(dirrectory,'images','Win_folder_icon.jpg'))
        open_folder_icon = qtg.QIcon(
            path.join(dirrectory, "images", "Win_open_folder.png")
        )
        open_folder_action = qtw.QAction(
            open_folder_icon, "Open", self, triggered=lambda: self.openImageFolder()
        )

        self.main_toolbar.addAction(open_folder_action)
        # self.main_toolbar.setToolButtonStyle(qtc.Qt.ToolButtonIconOnly)
        main_toolbar_stylesheet = """
        QToolBar {
            background-color : transparent; 
            border: 0px;
        }"""
        self.main_toolbar.setStyleSheet(main_toolbar_stylesheet)

        ##Test for tool bar##
        # self.main_toolbar.addAction("add")

        #####TO DO##################################

        #############################################



        ###################
        ###Layout##########
        ###################

    def openImageFolder(self):

        dialog = qtw.QFileDialog(self, "Open Image Folder")
        dialog.setDirectory(self.book_folder_path)
        dialog.setAcceptMode(qtw.QFileDialog.AcceptOpen)
        dialog.setFileMode(qtw.QFileDialog.DirectoryOnly)

        if dialog.exec():
            self.book_folder_path = dialog.selectedFiles()[0]

            # update the file_path in the setting.ini
            #self._config.set(
            #    SETTING_SECTION_PATHS, "open_file_path", str(self.book_folder_path)
            #)
            
            #setting_file = open(self._setting_file_path, "w")
            #self._config.write(setting_file)
            #setting_file.close()

            setting = qtc.QSettings(self.setting_path, qtc.QSettings.IniFormat)
            setting.setValue("User_settings/book_folder",self.book_folder_path)

            # update status bar and emit singal
            self._status_label.setText(str(self.book_folder_path))
            self.open_file_path.emit(str(self.book_folder_path))
            

    def closeEvent(self, closeEvent):
        # print('Enter close event')
        qsetting = qtc.QSettings(self.setting_path, qtc.QSettings.IniFormat)
        qsetting.setValue("MainWindow/geometry", self.saveGeometry())
        qsetting.setValue("MainWindow/windowState", self.saveState())
        # self._qsetting.clear()
        super().closeEvent(closeEvent)


if __name__ == "__main__":

    app = qtw.QApplication(sys.argv)
    dw = DebugWindow()
    mw = MainWindow()

    sys.exit(app.exec())
