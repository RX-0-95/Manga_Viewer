            def paintEvent(self, a0):
                opt = qtw.QStyleOption()
                opt.initFrom(self)
                painter = qtg.QPainter(self)
                self.style().drawPrimitive(qtw.QStyle.PE_Widget, opt, painter, self)
                super().paintEvent(a0)

Is needed when create a widget from QWidget and want use the style-sheet 