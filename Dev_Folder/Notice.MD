            def paintEvent(self, a0):
                opt = qtw.QStyleOption()
                opt.initFrom(self)
                painter = qtg.QPainter(self)
                self.style().drawPrimitive(qtw.QStyle.PE_Widget, opt, painter, self)
                super().paintEvent(a0)

Is needed when create a widget from QWidget and want use the style-sheet 


* Event Filter, install event filte to object 






# QT Bug Report 
1. The QGraphicsView and QGraphicsScene used in QMainwindow, when scroll to the end of the graphicsView, the wheel Event will pass to the QMainwindow, however, this even always trigger twice in QMainwindow 