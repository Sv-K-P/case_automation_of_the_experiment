### РАЗРАБОТКА НЕ ОКОНЧЕНА ###

import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt, QRectF, QPointF
from PyQt5.Qt import *

class tmpArea():
    def __init__(self):
        self.img_path = 'img/41uu2.png'
        self.name = 'Abrakadabra'

class AreaItem(QtWidgets.QWidget):
    def __init__(self, area):
        super().__init__()
        self.horisontalLayout = QtWidgets.QHBoxLayout()
        pixmap = QtGui.QPixmap(area.img_path)
        pixmap_label = QtWidgets.QLabel()
        pixmap_label.setPixmap(pixmap)
        # pixmap_label.resize()
        self.horisontalLayout.addWidget(pixmap_label)
        label_name = QtWidgets.QLabel()
        label_name.setText(area.name)
        self.horisontalLayout.addWidget(label_name)

class AreaList(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

    def AddArea(self, area):
        self.verticalLayout.addWidget(area)



def main():
    app = QtWidgets.QApplication(sys.argv)  
    window = AreaList()
    area = tmpArea()
    area_item = AreaItem(area)
    window.AddArea(area_item)
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()