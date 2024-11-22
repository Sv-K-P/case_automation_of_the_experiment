from PyQt5 import QtCore, QtGui, QtWidgets

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
            print(event.pos().toPoint())

    def paint(self, painter, option, widget):
        painter.setPen(self.pen())
        painter.setBrush(self.brush())
        if option.state & QtWidgets.QStyle.State_Selected: # изменение цвета при нажатии
            pen = self.pen()
            pen.setColor(QtCore.Qt.blue)
            painter.setPen(pen)
            painter.setBrush(QtCore.Qt.NoBrush)
        painter.drawRect(self.boundingRect())



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    scene = QtWidgets.QGraphicsScene(-400, -400, 800, 800)
    w = QtWidgets.QGraphicsView(scene)
    scene.addItem(smallRectangle(100, 100))
    w.show()
    sys.exit(app.exec_())