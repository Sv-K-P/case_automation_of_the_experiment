#defSettingsWindow.py

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.Qt import *

from areaList import *
from crop_image import *
from qtdesign.settings_window import Ui_SettingsWindow

list_area = []

class GraphicsView(QtWidgets.QGraphicsView):
    """
    Класс области с изображением
    """
    def __init__(self, parent=None):
        super().__init__(QtWidgets.QGraphicsScene(), parent)


        self.pixmap_item = self.scene().addPixmap(QtGui.QPixmap())

        self.pixmap_item.setShapeMode(QtWidgets.QGraphicsPixmapItem.BoundingRectShape)

        self.setAlignment(QtCore.Qt.AlignCenter)
        #self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def set_image(self, pixmap):
        #self.setFixedSize(pixmap.size())
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

        items = self.items(event.pos())

        if event.buttons() == Qt.LeftButton and self.flag:
            for item in items:
                if item is self.pixmap_item:
                    self.start_for_selection = event.pos()

                    self.start = item.mapFromScene(self.mapToScene(event.pos())).toPoint()
                    break


        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        items = self.items(event.pos())

        if event.buttons() == Qt.LeftButton and self.flag:
            for item in items:
                if item is self.pixmap_item:

                    self.end = item.mapFromScene(self.mapToScene(event.pos())).toPoint()
                    self.end_for_selection = event.pos()

                    self.selection.setGeometry(QtCore.QRect(self.start_for_selection, self.end_for_selection).normalized())
                    self.selection.show()
                    break

        return super().mouseMoveEvent(event)


    def mouseReleaseEvent(self, event):

        items = self.items(event.pos())

        if self.flag:

                    #self.end = item.mapFromScene(self.mapToScene(event.pos())).toPoint()
                self.flag = False
                self.selection.hide()

                size = QRectF(
                        QPointF(min(self.start.x(), self.end.x()), min(self.start.y(), self.end.y())),
                        QPointF(max(self.start.x(), self.end.x()), max(self.start.y(), self.end.y()))
                )
                area = CropItem(self.pixmap_item, size)
                list_area.append(area)
                print(list_area)

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

        ########################################

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LoadOriginalImage.sizePolicy().hasHeightForWidth())
        self.LoadOriginalImage.setSizePolicy(sizePolicy)
        self.LoadOriginalImage.setAutoRepeat(False)
        self.LoadOriginalImage.setAutoExclusive(False)
        self.LoadOriginalImage.setDefault(False)
        self.LoadOriginalImage.setFlat(False)

        ###############################################

        self.LoadOriginalImage.clicked.connect(self.takeImage) # настройка действий для кнопок
        self.MakeCroppedImage.clicked.connect(self.left_view.make)
        self.DeleteCroppedImage.clicked.connect(self.open_area_settings)

        ######################
 
    def open_area_settings(self):
        """
        Вызов списка выделенных областей и их настроек
        """
        self.list_area = ListArea()
        self.list_area.show()
        for i in range(len(list_area)):
            self.list_area.add_area(list_area[i])

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