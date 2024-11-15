import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *

from PyQt5.QtGui import QPainter, QPen, QImage
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QFileDialog
from PyQt5.QtCore import Qt, QRectF, QPointF

from PIL import ImageGrab  # +++
import num






class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(30, 30, 600, 400)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()

        mainMenu = self.menuBar()
        file = mainMenu.addMenu("Файл")
        instmenu = mainMenu.addMenu("Инстументы")

        photo = QAction("Вставить фото", self)
        file.addAction(photo)
        photo.triggered.connect(self.takeImage)  # подключаем функционал к кнопкам

        videlenie = QAction("ВыделитЬ", self)  # подключение выпадающий минушек
        instmenu.addAction(videlenie)
        videlenie.triggered.connect(self.screenshot)
        self.instrument = False
        self.selection = QRubberBand(QRubberBand.Rectangle, self)

        self.image_foreground = QImage(self.size(), QImage.Format_ARGB32_Premultiplied)  # картинка подключается
        self.image_foreground.fill(Qt.transparent)
        self.image_background = QImage()
        self.image_background.fill(Qt.white)

    def takeImage(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите изображение",
            "",
            "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*)"
        )
        if not filename:
            return
        self.image_background.load(filename)
        self.selection.hide()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(self.rect(), self.image_background, self.image_background.rect())
        painter.drawImage(self.image_foreground.rect(), self.image_foreground)

    ### описание селекции на нажитие мыши
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.instrument:
            self.start = event.pos()
            self._start = event.globalPos()
            print('start', self.start)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.instrument:
            self.end = event.pos()
            self.selection.setGeometry(QRect(self.start, self.end).normalized())
            self.selection.show()

    def mouseReleaseEvent(self, event):
        if self.instrument:
            self.end = event.pos()
            self._end = event.globalPos()
            self.selection.hide()
            cleaver = editable_outline(self, self.start.x(), self.start.y(), self.end.x(), self.end.y())
            cleaver.make_outline()
            print(cleaver.return_star_cord())

    ###

    def screenshot(self):
        if self.instrument:
            self.instrument = False
        else:
            self.instrument = True


"""# Нужно но не точно
    def resizeEvent(self, event): ### без этого не работает
        self.image_foreground = QImage(self.size(), QImage.Format_ARGB32_Premultiplied)
        self.image_foreground.fill(Qt.transparent)
        self.update()
        super().resizeEvent(event)
#"""

class editable_outline(MainWindow):
    def __init__(self, parent, x_start, y_start, x_end, y_end):
        QMainWindow.__init__(self, parent)
        self._x_start = x_start
        self._y_start = y_start
        self._x_end = x_end
        self._y_end = y_end

    def return_star_cord(self):
        return self._x_start, self._y_start

    def return_end_corf(self):
        return self._x_end, self._y_end

    def make_outline(self):
        self.button_left_top = QPushButton("test")
        self.button_left_top.resize(10, 10)
        self.button_left_top.move(self._x_start, self._y_start)
        self.button_left_top.show()



def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())