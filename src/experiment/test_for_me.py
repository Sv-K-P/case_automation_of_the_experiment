from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys


class ButtonMoveRectItem(QGraphicsRectItem):

    def __init__(self, position_flags, parent):
        QGraphicsRectItem.__init__(self, -3, -3, 10, 10, parent)
        # настройки цвета кнопки
        self.setBrush(QBrush(QColor(116, 110, 141, 250)))
        # self.setBrush(QBrush(QColor(81, 168, 220, 200)))
        self.setPen(QPen(
            QColor(0, 0, 0, 255),
            1.0,
            Qt.SolidLine,
            Qt.RoundCap,
            Qt.RoundJoin
        ))

        self._positionFlags = position_flags
        # педключаем флаги на перемещение с помощтю ЛКМ
        self.setFlag(self.ItemIsMovable)
        # уведомление о перемещении, возможно негативно влияет на оптимизацию, нужно проверить
        self.setFlag(self.ItemSendsGeometryChanges)

    # возращаем корд.

    def position_flags(self):
        return self._positionFlags

    # Это метод должен быть определен по стандартам библиотеки
    # change - флаг изменения, value - координаты новой позиции (локальные корд.)
    # ItemPositionChange - флаг, который мы получаем после перемещения

    def itemChange(self, change, value):
        return_value = value

        # обновляем границы сетки

        if change == self.ItemPositionHasChanged:
            if self.position_flags() == area_selection.Top:

                self.parentItem().set_Top(value.y())

            elif self.position_flags() == area_selection.TopRight:
                self.parentItem().set_TopRight(value)

            elif self.position_flags() == area_selection.Right:
                self.parentItem().set_Right(value.x())

            elif self.position_flags() == area_selection.BottomRight:
                self.parentItem().set_BottomRight(value)

            elif self.position_flags() == area_selection.Bottom:
                self.parentItem().set_Bottom(value.y())

            elif self.position_flags() == area_selection.BottomLeft:
                self.parentItem().set_BottomLeft(value)

            elif self.position_flags() == area_selection.Left:
                self.parentItem().set_Left(value.x())

            elif self.position_flags() == area_selection.TopLeft:
                self.parentItem().set_TopLeft(value)

        return return_value


class area_selection(QGraphicsItem):
    # Флаги отвечают за кнопки, то есть опр. конкретную кнопку
    # Нумирация начинается с верхней кнопки по середине. Далее по часовой стрелке

    Top = 1
    TopRight = 2
    Right = 3
    BottomRight = 4
    Bottom = 5
    BottomLeft = 6
    Left = 7
    TopLeft = 8

    def __init__(self, parent):
        QGraphicsItem.__init__(self, parent)

        # словарь курсоров

        handleCursors = {
            self.TopLeft: Qt.SizeFDiagCursor,
            self.Top: Qt.SizeVerCursor,
            self.TopRight: Qt.SizeBDiagCursor,
            self.Left: Qt.SizeHorCursor,
            self.Right: Qt.SizeHorCursor,
            self.BottomLeft: Qt.SizeBDiagCursor,
            self.Bottom: Qt.SizeVerCursor,
            self.BottomRight: Qt.SizeFDiagCursor,
        }

        # наследуем intern_rect из CropItem

        self.background_selection = QRectF(0, 0, 0, 0)

        if self.parentItem():
            self.background_selection = self.parentItem().rect()

        # иницилизируем кнопки и передаем их в массив

        self.list_of_button = [ButtonMoveRectItem(tags, self) for tags in
                               [self.Top, self.TopRight, self.Right, self.BottomRight, self.Bottom, self.BottomLeft,
                                self.Left, self.TopLeft]]

        # устанавливаем уникальный курсор для каждой кнопки

        for item in self.list_of_button:
            item.setCursor(handleCursors[item.position_flags()])

        self.updatePosition()

    def updatePosition(self):
        for item in self.list_of_button:
            # устанавливаем кнопки по границе background_selection

            if item.position_flags() == self.TopLeft:
                item.setPos(self.background_selection.topLeft())

            if item.position_flags() == self.Top:
                item.setPos(self.background_selection.left() + self.background_selection.width() // 2,
                            self.background_selection.top())

            if item.position_flags() == self.TopRight:
                item.setPos(self.background_selection.topRight())

            if item.position_flags() == self.Right:
                item.setPos(self.background_selection.right(),
                            self.background_selection.top() + self.background_selection.height() // 2)

            if item.position_flags() == self.BottomRight:
                item.setPos(self.background_selection.bottomRight())

            if item.position_flags() == self.Bottom:
                item.setPos(self.background_selection.left() + self.background_selection.width() // 2,
                            self.background_selection.bottom())

            if item.position_flags() == self.BottomLeft:
                item.setPos(self.background_selection.bottomLeft())

            if item.position_flags() == self.Left:
                item.setPos(self.background_selection.left(),
                            self.background_selection.top() + self.background_selection.height() // 2)

    # функции на переопределения параметров сетки, то есть параметров background_selection

    def set_Top(self, value):
        self.background_selection.setTop(value)
        self.doResize()

    def set_Right(self, value):
        self.background_selection.setRight(value)
        self.doResize()

    def set_Bottom(self, value):
        self.background_selection.setBottom(value)
        self.doResize()

    def set_Left(self, value):
        self.background_selection.setLeft(value)
        self.doResize()

    def set_TopLeft(self, value):
        self.background_selection.setTopLeft(value)
        self.doResize()

    def set_TopRight(self, value):
        self.background_selection.setTopRight(value)
        self.doResize()

    def set_BottomRight(self, value):
        self.background_selection.setBottomRight(value)
        self.doResize()

    def set_BottomLeft(self, value):
        self.background_selection.setBottomLeft(value)
        self.doResize()

    # обновляем сетку

    def doResize(self):
        self.parentItem().create_path()
        self.updatePosition()

    # функция необходимая по стандартам библиотеки, необходима для корректной работы программы

    def boundingRect(self):
        if self.parentItem():
            return self.background_selection
        else:
            return QRectF(0, 0, 0, 0)

    # рисуем сетку
    # функция необходимая по стандартам библиотеки, необходима для корректной работы программы

    def paint(self, painter, option, widget):
        painter.setRenderHint(QPainter.Antialiasing)
        # сделать метод который возращает цвет
        painter.setBrush(QBrush(QColor(110, 142, 132, 150)))
        painter.setPen(QPen(QColor(110, 142, 132), 2.0, Qt.DashLine))

        painter.drawRect(self.background_selection)


class CropItem(QGraphicsPathItem):
    def __init__(self, parent):
        QGraphicsPathItem.__init__(self, parent)
        # метод boundingRect вписывает любую фигуру в прямоугольник и возращает его координаты

        self._path = QPainterPath()
        self.extern_rect = parent.boundingRect()

        # Переопределяем переменную, создаем прямоугольник с плав. точкой, с соотв. корд.
        # тут мы задаем изначальные границы зоны
        # нужно переделать на пользовательские координаты
        self.intern_rect = QRectF(0, 0,
                                  self.extern_rect.width() / 2,
                                  self.extern_rect.height() / 2)

        # перемещаем в центр
        # тестовый функционал
        self.intern_rect.moveCenter(self.extern_rect.center())

        area_selection(self)
        self.create_path()

    # возращаем inter_rect

    def rect(self):
        return self.intern_rect

    # обновление inter_rect
    # объект QPainterPath позволяет повторно использовать сложную фигуру, без необходимости
    # повторной иницилизации фигуры

    def create_path(self):
        self._path = QPainterPath()
        self._path.addRect(self.extern_rect)
        self._path.moveTo(self.intern_rect.topLeft())
        self._path.addRect(self.intern_rect)
        self.setPath(self._path)


sys._excepthook = sys.excepthook


def my_exception_hook(error_type, value, traceback):
    # Print the error and traceback
    print(error_type, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(error_type, value, traceback)
    sys.exit(1)


# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = QGraphicsView()
    scene = QGraphicsScene()
    view.setScene(scene)
    view.setFixedSize(QPixmap("test.png").size())
    pixmapItem = scene.addPixmap(QPixmap("test.png"))

    cropItem = CropItem(pixmapItem)

    view.show()

    sys.exit(app.exec_())
