import zipfile
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import sys
import os
from .utilities import Utilities
from .filematch import FileMatch as fm

##################TOOL when develop#################
from .dev_tool import DebugWindow

#######################################

################TO DO#####################
# 1. test with heavy load opeation to see if multithread work (Done)
# 2. Consider write C++ based zip lib python module to get the best multithread performance

#################Dev#############################
# 1. read the cover to pixmap and put the pixmap to the QItem object (Done)
# 2. RegEx to make identify file type (Done)
# 3. When the zip file contains a folder(Done)


class BookCoverLoader(qtc.QObject):
    finished = qtc.pyqtSignal()
    cover_changed = qtc.pyqtSignal(qtc.QModelIndex)

    def __init__(self, book_model):
        super().__init__()
        self.book_model = book_model

    @qtc.pyqtSlot(list, list)
    def do_load_cover(self, file_info_list, index_list):
        # when t
        for (index, file_info) in zip(index_list, file_info_list):
            file_path = file_info.absoluteFilePath()
            item = self.book_model.itemFromIndex(index)
            if file_info.isDir():
                image = qtg.QPixmap(Utilities.getWinOpenFolderPath())
                item.setCover(image)
                self.cover_changed.emit(index)
                continue
            try:
                zf = zipfile.ZipFile(file_path)
                image = qtg.QImage()

                firstFilename = zf.namelist()[0]
                if fm.isImage(firstFilename):
                    image.loadFromData(zf.open(firstFilename).read())
                # if there is a folder inside the zipfile

                if image.isNull():
                    for filename in zf.namelist():
                        if fm.isImage(filename):
                            image.loadFromData(zf.open(filename).read())
                            break

                image = image.scaledToWidth(200, qtc.Qt.SmoothTransformation)

                self.book_model.itemFromIndex(index).setCover(
                    qtg.QPixmap.fromImage(image)
                )
                # self.book_model.dataChanged()
                # print(f'image size: {image.sizeInBytes()} bytes ')
                # self.book_model.item(row).setCover(pixmap)
                self.cover_changed.emit(index)
                zf.close()
            except Exception as e:
                print(f"Exception: {e}")
                print(f"filename: {file_info.absoluteFilePath()}")
        self.finished.emit()


##########################Potential Version when Zipfile code is rewritten#########################


class ZipBookCoverReader(qtc.QRunnable):
    file_lock = qtc.QMutex()

    def __init__(self, item, zipFilePath):
        super().__init__()
        self.item = item
        self.zipFilePath = zipFilePath
        self.pixmap = qtg.QPixmap(300, 300)

    def run(self):
        zf = zipfile.ZipFile(self.zipFilePath)
        for file in zf.namelist():
            print(f"filename: {file}")

        print(f"fist file:{zf.namelist()[0]} ")
        data = zf.open(zf.namelist()[0]).read()
        zf.close()

        self.pixmap.loadFromData(data)

        self.item.setCover(self.pixmap)


# class used to manage the reader
class ReadCoverManager(qtc.QObject):
    finished = qtc.pyqtSignal()

    def __init__(self, model, thread_count=3):
        super().__init__()
        self.pool = qtc.QThreadPool.globalInstance()
        self.pool.setMaxThreadCount(thread_count)
        self.model = model

    @qtc.pyqtSlot(str)
    def do_read(self, source):
        qdir = qtc.QDir(source)
        print(source)
        for i, filename in enumerate(qdir.entryList(qtc.QDir.Files)):
            filepath = qdir.absoluteFilePath(filename)
            print(f"filepath{filepath}")
            runner = ZipBookCoverReader(self.model.item(i), filepath)
            self.pool.start(runner)

        # for i, fileInfo in enumerate(fileInfoList):
        #    path = fileInfo.absoluteFilePath()
        #    runner = ZipBookCoverReader(model.item(i),path)
        #    self.pool.start(runner)

        self.pool.waitForDone()
        self.finished.emit()

    @qtc.pyqtSlot(list)
    def print_list(self, list):
        for ele in list:
            print(f"list: {ele.absoluteFilePath()}")


if __name__ == "__main__":
    filename = "absc"
    # pattern = re.compile(r'*\.jpg$')
    # match  = pattern.search(filename)
    match = re.match(r".*\.jpg|.*\.png$", filename)
    print(match)
    if filename == "*.png":
        print("dsafdsf")

