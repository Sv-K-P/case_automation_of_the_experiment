#defSettingsWindow.py

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog

from qtdesign.settings_window import Ui_SettingsWindow

point_filename = 'img/41uu2.png'


class smallRectangle(QtWidgets.QGraphicsRectItem):
    def __init__(self, x, y, w=10, h=10):
        super(smallRectangle, self).__init__(0, 0, w, h)
        self.setPen(QtGui.QPen(QtCore.Qt.red, 2))
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsSelectable
            | QtWidgets.QGraphicsItem.ItemIsMovable
            | QtWidgets.QGraphicsItem.ItemIsFocusable
            | QtWidgets.QGraphicsItem.ItemSendsGeometryChanges
            | QtWidgets.QGraphicsItem.ItemSendsScenePositionChanges)
        self.setPos(QtCore.QPointF(x, y))

    def mouseMoveEvent(self, event): # обработчик нажатия и движения мыши
        if event.buttons() & QtCore.Qt.LeftButton:
            super(smallRectangle, self).mouseMoveEvent(event)
            # print(event.pos().toPoint())

    def paint(self, painter, option, widget):
        painter.setPen(self.pen())
        painter.setBrush(self.brush())
        if option.state & QtWidgets.QStyle.State_Selected: # изменение цвета при нажатии
            pen = self.pen()
            pen.setColor(QtCore.Qt.blue)
            painter.setPen(pen)
            painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawRect(self.boundingRect())

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
        self.pixmap_item.setPixmap(pixmap)
        self.fitInView(self.pixmap_item, QtCore.Qt.KeepAspectRatio)

class CropView(GraphicsView):
    """
    Класс для области с обрезаемым изображением, реализация обрезки
    """    
    resultChanged = QtCore.pyqtSignal(QtGui.QPixmap)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.point_items = [] # массив с вершинами прямоугольника

    def mousePressEvent(self, event: QtGui.QMouseEvent | None) -> None:
        print(event.pos().x(), event.pos().y())
        point = smallRectangle(event.pos().x(), event.pos().y())
        self.scene().addItem(point)
        self.point_items.append(point)
        return super().mousePressEvent(event)

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
        self.rigth_view = GraphicsView()

        self.HLayoutImage = QtWidgets.QHBoxLayout() # добавление горизонтальных компоновщиков для картинок и для кнопок
        self.HLayoutImage.setObjectName("HLayoutImage")
        self.verticalLayout_3.addLayout(self.HLayoutImage)
        self.HLayoutButton = QtWidgets.QHBoxLayout()
        self.HLayoutButton.setObjectName("HLayoutButton")
        self.verticalLayout_3.addLayout(self.HLayoutButton)

        self.HLayoutImage.addWidget(self.left_view) # встраивание областей с изображениями
        self.HLayoutImage.addWidget(self.rigth_view)

        self.LoadOriginalImage = QtWidgets.QPushButton(self.GeneralSettings) # определение кнопок
        self.LoadOriginalImage.setObjectName("LoadOriginalImage")
        self.HLayoutButton.addWidget(self.LoadOriginalImage)
        self.SaveCroppedImage = QtWidgets.QPushButton(self.GeneralSettings)
        self.SaveCroppedImage.setObjectName("SaveCroppedImage")
        self.HLayoutButton.addWidget(self.SaveCroppedImage)
        self.DeleteCroppedImage = QtWidgets.QPushButton(self.GeneralSettings)
        self.DeleteCroppedImage.setObjectName("DeleteCroppedImage")
        self.HLayoutButton.addWidget(self.DeleteCroppedImage)

        _translate = QtCore.QCoreApplication.translate # настройка надписей
        self.LoadOriginalImage.setText(_translate("SettingsWindow", "Получить изображение"))
        self.SaveCroppedImage.setText(_translate("SettingsWindow", "Сохранить область"))
        self.DeleteCroppedImage.setText(_translate("SettingsWindow", "Удалить область"))

        self.LoadOriginalImage.clicked.connect(self.takeImage) # настройка действий для кнопок
        self.SaveCroppedImage.clicked.connect(self.ViewCropped)
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
        self.rigth_view.set_image(self.left_view.resulted)