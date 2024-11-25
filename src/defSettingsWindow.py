#defSettingsWindow.py

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.Qt import *

from test_for_me import *
from qtdesign.settings_window import Ui_SettingsWindow

point_filename = 'img/41uu2.png'


class GraphicsView(QtWidgets.QGraphicsView):
    """
    Класс области с изображением
    """
    def __init__(self, parent=None):
        super().__init__(QtWidgets.QGraphicsScene(), parent)


        self.pixmap_item = self.scene().addPixmap(QtGui.QPixmap())

        self.pixmap_item.setShapeMode(QtWidgets.QGraphicsPixmapItem.BoundingRectShape)

        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def set_image(self, pixmap):
        self.setFixedSize(pixmap.size())
        self.pixmap_item.setPixmap(pixmap)



class CropView(GraphicsView):
    """
    Класс для области с обрезаемым изображением, реализация обрезки
    """    
    resultChanged = QtCore.pyqtSignal(QtGui.QPixmap)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.flag = True
        self.point_items = [] # массив с вершинами прямоугольника
        self.selection = QRubberBand(QRubberBand.Rectangle, self)

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.flag:
            self.start = event.pos()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.flag:
            self.end = event.pos()
            self.selection.setGeometry(QtCore.QRect(self.start, self.end).normalized())
            self.selection.show()
        return super().mouseMoveEvent(event)


    def mouseReleaseEvent(self, event):
        if self.flag:

            self.flag = False
            self.end = event.pos()

            self.selection.hide()
            size = QRectF(QPointF(min(self.start.x(), self.end.x()), min(self.start.y(), self.start.y())),
                          QPointF(max(self.start.x(), self.end.x()), max(self.start.y(), self.end.y())))
            CropItem(self.pixmap_item, size)
        return super().mouseReleaseEvent(event)

    def make(self):
        self.flag = True



class ExampleSet(QtWidgets.QMainWindow, Ui_SettingsWindow):
    """
    Класс для инициализации окна с настройками устройства
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()

        # Дополнение дизайна #
        self.left_view = CropView()


        self.HLayoutImage = QtWidgets.QHBoxLayout() # добавление горизонтальных компоновщиков для картинок и для кнопок
        self.HLayoutImage.setObjectName("HLayoutImage")
        self.verticalLayout_3.addLayout(self.HLayoutImage)
        self.HLayoutButton = QtWidgets.QHBoxLayout()
        self.HLayoutButton.setObjectName("HLayoutButton")
        self.verticalLayout_3.addLayout(self.HLayoutButton)

        self.HLayoutImage.addWidget(self.left_view) # встраивание областей с изображениями


        self.LoadOriginalImage = QtWidgets.QPushButton(self.GeneralSettings) # определение кнопок
        self.LoadOriginalImage.setObjectName("LoadOriginalImage")
        self.HLayoutButton.addWidget(self.LoadOriginalImage)
        self.MakeCroppedImage = QtWidgets.QPushButton(self.GeneralSettings)
        self.MakeCroppedImage.setObjectName("SaveCroppedImage")
        self.HLayoutButton.addWidget(self.MakeCroppedImage)
        self.DeleteCroppedImage = QtWidgets.QPushButton(self.GeneralSettings)
        self.DeleteCroppedImage.setObjectName("DeleteCroppedImage")
        self.HLayoutButton.addWidget(self.DeleteCroppedImage)

        _translate = QtCore.QCoreApplication.translate # настройка надписей
        self.LoadOriginalImage.setText(_translate("SettingsWindow", "Получить изображение"))
        self.MakeCroppedImage.setText(_translate("SettingsWindow", "Создать область"))
        self.DeleteCroppedImage.setText(_translate("SettingsWindow", "Удалить область"))

        self.LoadOriginalImage.clicked.connect(self.takeImage) # настройка действий для кнопок
        self.MakeCroppedImage.clicked.connect(self.left_view.make)
        ######################

    @QtCore.pyqtSlot()
    def takeImage(self):
        """
        Вызов окна для выбора файла (временное решение)
        """
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите изображение",
            "",
            "PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*)"
        )
        if filename:
            pixmap = QtGui.QPixmap(filename)
            self.left_view.set_image(pixmap)
    
    def ViewCropped(self):
        """
        Обрезка изображения и отображение результата

        :bug Если картинка не выбрана или не обозначены все 2 точки
        """
        self.rigth_view.set_image(self.left_view.resultChanged)

