from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from configparser import ConfigParser
import sys
from os import path

from zipBookReader import BookCoverLoader
from dev_tool import DebugWindow


SETTING_FILE = "setting.ini"
SETTING_SECTION_PATHS = "Paths"


########################
###BoonItem Variable####
########################
BI_DEFAULT_ICON = "book_loading.jpg"



from utilities import Utilities


class BookCoverDelegate(qtw.QStyledItemDelegate):
    def createEditor(self, parent, option, proxyModelIndex):
        # date_inp = qtw.QDateEdit(parent, calendarPopup=True)
        # date_inp.setCalendarPopup(True)
        return None

    ####################TO DO#################
    # 1.Move all the rect calculate and pixmap resize to BookItem class
    # 2. Override the paint for the project
    # 3. Consider use createEditor instead of paint
    # 4. Consider to create a book cover widget and use it in editor
    # 5. Use propotion instead of int to represent size to make program resolution independent
    def paint(self, painter, option, index):

        ########Some Print Setting################
        progress_bar_height = 5
        text_rect_padding = 5

        # Get the current iten
        current_item = index.model().itemFromIndex(index)

        c_x = option.rect.x()
        c_y = option.rect.y()
        c_width = option.rect.width()
        c_height = option.rect.height()
        #painter.drawRect(option.rect)
        # painter.drawRect()

        # calculate the cover sections rect
        cover_rect_width = c_width
        cover_rect_height = int(0.75 * c_height)
        cover_rect = qtc.QRect(c_x, c_y, cover_rect_width, cover_rect_height)

        # Set the cover to temp version
        ##### TO DO: load the cover in another thread
        ####Calcuate the proper place to draw the cover 
        

        if current_item.getCover():
            img = current_item.getCover()
            fit_size = img.size().scaled(cover_rect_width,cover_rect_height,
                qtc.Qt.KeepAspectRatio)
            
            fit_rect = qtc.QRect(
                c_x+int((cover_rect_width-fit_size.width()+1)/2),
                c_y + int((cover_rect_height-fit_size.height()+1)/2),
                fit_size.width(), fit_size.height())

            painter.drawPixmap(fit_rect, img)     
        else:
            cover = qtg.QPixmap(Utilities.getDefaultCoverPath())
            painter.drawPixmap(cover_rect, cover)

        #painter.drawPixmap(cover_rect.x(),cover_rect.y(),
        #   cover_rect.width(), cover_rect.height(),cover,0,0,0,0)

        # calculate the progress bar rect
        progress_bar_rect = qtc.QRect(
            cover_rect.bottomLeft().x(),
            cover_rect.bottomLeft().y(),
            c_width,
            progress_bar_height,
        )

        # Draw the progress bar
        progress_bar_opt = qtw.QStyleOptionProgressBar()
        progress_bar_opt.rect = progress_bar_rect
        progress_bar_opt.minimum = 0
        progress_bar_opt.maximum = 100
        progress_bar_opt.progress = index.model().itemFromIndex(index).getProgress()
        qtw.QApplication.style().drawControl(
            qtw.QStyle.CE_ProgressBar, progress_bar_opt, painter
        )

        # calculate the text rect
        text_rect = qtc.QRect(
            progress_bar_rect.bottomLeft().x(),
            progress_bar_rect.bottomLeft().y(),
            c_width,
            c_height - cover_rect.height() - progress_bar_rect.height(),
        )

        # Set the text field in the cover
        text_rect_padded = qtc.QRect(
            text_rect.x() + text_rect_padding,
            text_rect.y() + text_rect_padding,
            text_rect.width() - 2 * text_rect_padding,
            text_rect.height() - 2 * text_rect_padding,
        )

        # Add the text to the cover, ensure when text is out of bound, elided the text
        ######TO DO : create proper elideText class to solve text problem
        painter.fillRect(text_rect_padded, qtg.QColor("gray"))
        font_metrics = painter.fontMetrics()
        effective_width = (
            int(text_rect_padded.height() / font_metrics.height())
        ) * text_rect_padded.width() - font_metrics.width("xxx")
        bookname = str(current_item.getBookName())
        bookname = font_metrics.elidedText(bookname, qtc.Qt.ElideRight, effective_width)
        painter.drawText(
            text_rect_padded, qtc.Qt.AlignCenter | qtc.Qt.TextWrapAnywhere, bookname
        )

        # return super().paint(painter, option, index)


class BookItem(qtg.QStandardItem):
    def __init__(self, book_name=None, zipfile_path=None, width=300/2, height=int(350/2)):
        super().__init__()
        ####TO DO#######
        # decide whether to leave the book_name = None

        self.zipfile_path = zipfile_path
        self.item_type = None
        self.book_name = book_name
        self.book_cover = None

        self.setData(qtg.QPixmap(width, height), qtc.Qt.DecorationRole)

        self.progress = 0
        self.__width = width
        self.__height = height

    def setCover(self, cover):
        self.book_cover = cover
        # print('set Cover')
        self.emitDataChanged()

    def getCover(self):
        return self.book_cover

    def getBookName(self):
        return self.book_name

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def resize(self, width, height):
        self.__width = width
        self.__height = height
        #####TO DO: Resize the cover base on the current data#######
        self.setData(qtg.QPixmap(width, height), qtc.Qt.DecorationRole)
        self.emitDataChanged()

    def updateProgress(self, progress):
        self.progress = progress

        self.emitDataChanged()

    def getProgress(self):
        return self.progress

    def changeBookName(self, name):
        self.book_name = name
        self.updateItem()

    def setItemSize(self, size):
        None

    # Create an Item form a zip file
    @classmethod
    def fromZipFile(cls, zipFile):
        None

    # Open the
    @qtc.pyqtSlot()
    def openImage(self):
        None

    @qtc.pyqtSlot()
    def setZipFile(self, path):
        self.zipfile_path = path
        # update the icon

    @qtc.pyqtSlot()
    def updateItem(self):
        self.emitDataChanged()

###############TO DO: Stop the load cover thread when Image Folder is reload 
class BookShelfModel(qtg.QStandardItemModel):
    #######################
    ########signals########
    #######################
    # emit the signal to load the cover [fileInfo lsit][model_index list]
    cover_loader_sgn = qtc.pyqtSignal(list, list)
    # emit when folder load books, send the folder patg out
    folder_chage_sgn = qtc.pyqtSignal(str)
    #send the count of the book and folder
    file_count_sgn = qtc.pyqtSignal(int,int)

    quit_loader_thread = qtc.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        # member data
        self.book_folder_path = None

        ####Use the bookCover loader
        self.book_cover_loader = BookCoverLoader(self)
        self.loader_thread = qtc.QThread()
        self.book_cover_loader.moveToThread(self.loader_thread)
        self.loader_thread.start()
        self.cover_loader_sgn.connect(lambda: self.loader_thread.start())
        self.cover_loader_sgn.connect(self.book_cover_loader.do_load_cover)
        self.book_cover_loader.finished.connect(self.loader_thread.quit)
        self.book_cover_loader.cover_changed.connect(self.itemFromIndexUpdated)

    #########TO DO: filter the file before add to item, only zip, folder is allowed at this time#############

    @qtc.pyqtSlot(str)
    def loadBooks(self, book_folder_path):
        #Stop the current load cover thread first 
        
        ######Create BookItem#####
        directory = path.dirname(__file__)
        icon_path = path.join(directory, "images", "book_loading.jpg")
        book_load_icon = qtg.QIcon(qtg.QPixmap(icon_path))
        self.book_folder_path = book_folder_path
        self.folder_chage_sgn.emit(book_folder_path)
        #################debug######################
       

        #################End debug#################

        #################Add Item from Folder##############################
        # clear the model
        self.clear()
        
        # udpate the model
        book_dir = qtc.QDir(book_folder_path)
        # get .zip file
        name_filter = ["*.zip"]
        zip_file_info_list = book_dir.entryInfoList(
            name_filter,
            qtc.QDir.NoDotAndDotDot | qtc.QDir.Files | qtc.QDir.Dirs,
            qtc.QDir.Name
        )
      
        # get folder
        folder_file_info_list = book_dir.entryInfoList(
            qtc.QDir.NoDotAndDotDot | qtc.QDir.Dirs, qtc.QDir.Name
        )

        #get jpg, png, peng 
        name_filter = ["*.jpg","*.png"]
        img_file_info_list = book_dir.entryInfoList(
            name_filter,
            qtc.QDir.NoDotAndDotDot| qtc.QDir.Files,
            qtc.QDir.Name
        )
        #set the firt image as cover
        if img_file_info_list:
            print("inside")
            dir_cover = qtg.QPixmap(img_file_info_list[0].absoluteFilePath())
            book_item = BookItem(book_dir.dirName(),book_dir)
            book_item.setCover(dir_cover)
            self.appendRow(book_item)
        #emit the count of the file: book, folder
        self.file_count_sgn.emit(len(zip_file_info_list), len(folder_file_info_list))
        
        # combine the folder list and zip list
        file_info_list = folder_file_info_list + zip_file_info_list

        # for file_info in file_info_list:
        #    print(f"filename: {file_info.baseName()}")

        # create all bookitems and load the defaul cover
        default_cover_path = Utilities.getDefaultCoverPath()
        default_cover = qtg.QPixmap(default_cover_path)

        model_index_list = []
        for file_info in file_info_list:
            # Set the book cover for each item
            basename = file_info.baseName()
            book_item = BookItem(basename, file_info.absoluteFilePath())
            book_item.setCover(default_cover)
            self.appendRow(book_item)
            model_index_list.append(self.indexFromItem(book_item))

        # Read all the cover of the book from zip file
        # set those cover to the book cover, in another
        # thread
        self.cover_loader_sgn.emit(file_info_list, model_index_list)

    ###Force update the model from the giving index
    @qtc.pyqtSlot(qtc.QModelIndex)
    def itemFromIndexUpdated(self, index):
        self.dataChanged.emit(index, index)


###############TO DO##################
# Multithread method the load the books
class BookShelfView(qtw.QListView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFlow(qtw.QListView.LeftToRight)
        self.setViewMode(qtw.QListView.IconMode)
        self.setResizeMode(qtw.QListView.Adjust)
        self.setSpacing(5)
        self.setWrapping(True)
        self.delegate = BookCoverDelegate()
        self.setItemDelegate(self.delegate)
        # self.setGridSize(qtc.QSize(300,400))
        self.setSelectionRectVisible(True)




    # Open the choosen book in a viewer Window
    def openBook(self):
        None




########Book Shelf##########################
# Use bookshelf
class BookShelf(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(qtw.QFormLayout())
        self.books_model = BookShelfModel(self)
        self.books_view = BookShelfView(self)
        self.books_view.setModel(self.books_model)
        self.layout().addRow(self.books_view)
        #self.getView().setStyleSheet("background-color:gray;")

    def getView(self):
        return self.books_view

    def getModel(self):
        return self.books_model

    @qtc.pyqtSlot(str)
    def loadBooks(self, folder_path):
        # use BookShelf_model's load book fucntion
        self.books_model.loadBooks(folder_path)

        # load cover without thread

        # Load all cover in another thread

    @qtc.pyqtSlot(qtc.QModelIndex)
    def updateBookProgressFromIndex(self, index):
        # print(f"index: {index.row()}, {index.column()}")
        # print(self.books_model.itemFromIndex(index))
        item = self.books_model.itemFromIndex(index)
        # print(f"Ini progress: {item.getProgress()}")
        item.updateProgress(50)
        # print(f"after progress: {item.getProgress()}")

    #######Test use#####################
    #######update to proper function later################
    @qtc.pyqtSlot(qtc.QModelIndex)
    def updateCover(self, index):
        # print('setCover')
        item = self.books_model.itemFromIndex(index)
        cover = qtg.QPixmap(Utilities.getWinOpenFolderPath())
        item.setCover(cover)

    ### TO DO: refresh the books view
    def refresh(self):
        None

    ###TO DO: open an Item from its index (Dir or zip file)
    def openItemFromIndex(self, index):
        None