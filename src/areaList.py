#areaList.py

import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.Qt import *
from crop_image import CropItem


class Area():
    """
    Класс для описания области интереса (координат, миниатюр и т.д.)
    """
    def __init__(self):
        self.name = ''
        self.coord = []
        self.path_to_img = ''
        self.type = '' # 'num' or 'arrow'
    
    def setting(self, name: str, coord: list | tuple, path: str, type: str):
        self.name = name
        self.coord = coord
        self.path_to_img = path
        self.type = type
    


class GraphicsViewL(QtWidgets.QGraphicsView):
    """
    Класс области с изображением для вставки в виджет
    """
    def __init__(self, parent=None):
        super().__init__(QtWidgets.QGraphicsScene(), parent)

        self.pixmap_item = self.scene().addPixmap(QtGui.QPixmap())
        self.pixmap_item.setShapeMode(QtWidgets.QGraphicsPixmapItem.BoundingRectShape)

        self.setAlignment(QtCore.Qt.AlignCenter)

    def set_image(self, pixmap):
        self.setFixedSize(QtCore.QSize(300, 200))
        self.pixmap_item.setPixmap(pixmap)



class ListAreaItem(QtWidgets.QWidget):
    """
    Виджет содержащий горизонтальный компоновщик с миниатюрой, названием и кнопкой открытия настроек
    """
    def __init__(self, area: CropItem):
        super().__init__()

        origin_img_path = 'cat.jpeg'

        pixmap = QtGui.QPixmap(origin_img_path)
        print(pixmap.isNull())

        self.miniature = GraphicsViewL()
        print(pixmap.isNull())
        self.miniature.set_image(pixmap.copy(area.return_cords()))

        self.preference = QtWidgets.QPushButton('Настройки')

        self.nameLabel = QtWidgets.QLabel()
        self.nameLabel.setText('abrakadabra')

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addWidget(self.miniature)
        main_layout.addWidget(self.nameLabel)
        main_layout.addWidget(self.preference)

        self.setLayout(main_layout)

class ListArea(QtWidgets.QWidget):
    """
    Виджет, представляющий собой список ListAreaItems
    """
    def __init__(self):
        super().__init__()

        self.layout_item = QtWidgets.QVBoxLayout()
        self.layout_item.addStretch()

        self.frame = QtWidgets.QFrame()
        self.frame.setMinimumSize(200, 200)
        self.frame.setFrameStyle(QtWidgets.QFrame.Box)
        self.frame.setLayout(self.layout_item)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.frame)

        self.setLayout(main_layout)

    def add_area(self, area: CropItem):
        """
        Добавление элемента в список
        """
        item = ListAreaItem(area)
        self.layout_item.insertWidget(0, item)