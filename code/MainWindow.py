import sys, os

from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.Qt import *

from PyQt5.QtGui import QPainter, QImage, QBrush, QPen
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QRubberBand
from PyQt5.QtCore import Qt, QRect

point_filename = "../img/41uu2.png"

class GraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(QtWidgets.QGraphicsScene(), parent)
        self.pixmap_item = self.scene().addPixmap(QtGui.QPixmap())
        self.pixmap_item.setShapeMode(QtWidgets.QGraphicsPixmapItem.BoundingRectShape)

        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

    def set_image(self, pixmap):
        self.pixmap_item.setPixmap(pixmap)
        self.fitInView(self.pixmap_item, QtCore.Qt.KeepAspectRatio)

class CropView(GraphicsView): # the class of the cropped image from the device
    resultChanged = QtCore.pyqtSignal(QtGui.QPixmap)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.point_items = [] # array of point rectangle

    def mousePressEvent(self, event):
        if not self.pixmap_item.pixmap().isNull(): 
            sp = self.mapToScene(event.pos())
            lp = self.pixmap_item.mapFromScene(sp)
            if self.pixmap_item.contains(lp):
                size = QtCore.QSize(30, 30)
                height = (
                    self.mapToScene(QtCore.QRect(QtCore.QPoint(), size))
                    .boundingRect()
                    .size()
                    .height()
                )
                pixmap = QtGui.QPixmap(point_filename) # draw point
                point_item = QtWidgets.QGraphicsPixmapItem(pixmap, self.pixmap_item)

                point_item.setOffset( # append points to array
                    -QtCore.QRect(QtCore.QPoint(), pixmap.size()).center()
                )
                point_item.setPos(lp)
                scale = height / point_item.boundingRect().size().height()
                point_item.setScale(scale)
                self.point_items.append(point_item)

                if len(self.point_items) == 2:
                    points = []
                    for i in self.point_items:
                        points.append(i.pos().toPoint())
                    self.crop(points)
                elif len(self.point_items) == 3:
                    for i in self.point_items[:-1]:
                        self.scene().removeItem(i)
                    self.point_items = [self.point_items[-1]]
            else:
                print("outside")
        super().mousePressEvent(event)

    def crop(self, old_points: list):
        points = [old_points[0], QtCore.QPoint(old_points[1].x(), old_points[0].y()) , old_points[1], QtCore.QPoint(old_points[0].x(), old_points[1].y())]
        print(points) # отладочное
        
        polygon = QtGui.QPolygonF(points)
        path = QtGui.QPainterPath()
        path.addPolygon(polygon)

        source = self.pixmap_item.pixmap()

        r = path.boundingRect().toRect().intersected(source.rect())

        pixmap = QtGui.QPixmap(source.size())
        pixmap.fill(QtCore.Qt.transparent)
        painter = QtGui.QPainter(pixmap)
        painter.setClipPath(path)
        painter.drawPixmap(QtCore.QPoint(), source, source.rect())
        painter.end()
        result = pixmap.copy(r)
        self.resultChanged.emit(result)
        self.resulted = result

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(30, 30, 600, 400)

        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()

        self.left_view = CropView()
        self.rigth_view = GraphicsView()

        button = QtWidgets.QPushButton(self.tr("Резня!"))
        button.setFixedSize(230, 60)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        button.setFont(font)
        button.clicked.connect(self.ViewCropped)

### Define Top Menu ###
        mainMenu = self.menuBar()
        file_menu = mainMenu.addMenu("Файл")
        inst_menu = mainMenu.addMenu("Инстументы")

        photo = QAction("Вставить фото", self)
        file_menu.addAction(photo)
        photo.triggered.connect(self.takeImage)

        videlenie = QAction("Выделить", self)
        inst_menu.addAction(videlenie)
########################

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        lay = QtWidgets.QGridLayout(central_widget)
        lay.addWidget(self.left_view, 0, 0)
        lay.addWidget(self.rigth_view, 0, 1)
        lay.addWidget(button, 1, 0, 1, 2, alignment=QtCore.Qt.AlignHCenter)

    @QtCore.pyqtSlot()
    def takeImage(self):
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
        self.rigth_view.set_image(self.left_view.resulted)