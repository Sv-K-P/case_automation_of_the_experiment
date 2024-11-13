import sys
from PyQt5 import QtWidgets

import  start_window

class ExampleApp(QtWidgets.QMainWindow, start_window.Ui_MainWindow): # тк файл с дизайном постоянно перезаписывается, мы не будем его изменять, а создадим новый класс
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # инициализация дизайна

def main():
    app = QtWidgets.QApplication(sys.argv)  
    window = ExampleApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()