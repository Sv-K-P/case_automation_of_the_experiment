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
    def __init__(self, name):
        super().__init__()
        self.setupUi(self)

        self.deviceName = name # имя устройства, для которого были открыты настройки
        self.device_idx = -1

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
        self.DeleteCroppedImage.setText(_translate("SettingsWindow", "Менеджер областей"))

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

        self.ChangeNameLine.setText(self.deviceName) # настройка действий для блока общих настроек и значений при запуске
        self.conf_arr = []
        with open('config/device_config.csv', mode='r') as f:
            for s in f.readlines():
                self.conf_arr.append(s.split(','))
            self.device_idx = 0 # определяем индекс выбранного устройства в конфиге
            for i in range(len(self.conf_arr)):
                if self.conf_arr[i][0] == self.deviceName:
                    self.device_idx = i
                    self.numberDevice.setValue(int(self.conf_arr[i][1]))
            

        self.ChangeNameLine.editingFinished.connect(self.change_name)
        self.numberDevice.valueChanged.connect(self.change_num_camera)
        self.changeStorageFile.clicked.connect(self.change_starage_path)
        ######################
 
    def open_area_settings(self):
        """
        Вызов списка выделенных областей и их настроек
        """
        self.list_area = ListArea()
        self.list_area.show()
        for i in range(len(list_area)):
            self.list_area.add_area(list_area[i])

    def change_device_preference(self, field, value):
        """
        Перезапись файла настроек

        :param field: Поле в конфиге, которое необходимо изменить
        :param value: Значение на которое меняем
        """
        with open('config/device_config.csv', mode='r') as f:
            if field == 'name':
                self.conf_arr[self.device_idx][0] = value
                self.deviceName = value
            elif field == 'num_cumera':
                self.conf_arr[self.device_idx][1] = value
            elif field == 'storage_path':
                self.conf_arr[self.device_idx][2] = value
        with open('config/device_config.csv', mode='w') as f:
            for c in self.conf_arr:
                f.write(','.join(c))

    def change_name(self): # вспомогательные функции-обертки для change_device_preference
        self.change_device_preference(field='name', value=self.ChangeNameLine.text())

    def change_num_camera(self):
        self.change_device_preference(field='num_cumera', value=str(self.numberDevice.value()))

    def change_starage_path(self):
        self.change_device_preference(field='storage_path', value=str(self.takeImage()))

    @QtCore.pyqtSlot()
    def takeImage(self):
        """
        Вызов окна для выбора файла
        """
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл",
            "",
            "All Files(*.*)"
        )
        if filename:
            return filename