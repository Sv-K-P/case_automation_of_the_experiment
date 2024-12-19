#main.py

import sys
from PyQt5 import QtWidgets

from qtdesign import start_window
from connection_list import Device
from areaList import ListArea

list_connection = [] # необходимо сохранять соответсвие индексов с DeviceList



class ExampleApp(QtWidgets.QMainWindow, start_window.Ui_MainWindow):
    """
    Тк файл с дизайном постоянно перезаписывается, мы не будем его изменять, а создадим новый класс
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)  ### инициализация и дополнение дизайна
        # self.OpenAreaSettings = QtWidgets.QPushButton()
        # self.horizontalLayout.addWidget(self.OpenAreaSettings)
        # self.OpenAreaSettings.setText('Выделенные области')
        ###

        with open('config/device_config.csv', mode='r') as f:
            for s in f.readlines():
                line = s.split(',')
                device = Device(line[0])
                device.build_connection()
                list_connection.append(device)
                self.DeviceList.addItem(device.name)

        self.NewConnection.clicked.connect(self.new_connection) # назначение кнопок
        self.OpenSettings.clicked.connect(self.open_settings)
        self.DeleteConnection.clicked.connect(self.delete_connection)
        # self.OpenAreaSettings.clicked.connect(self.open_area_settings)

        self.DeviceList.itemSelectionChanged.connect(self.selectionChanged) # обработка выбора в QListWidget
        self.idx = 0 # индекс выбранного в данный момент элемента

    def selectionChanged(self):
        """
        Вспомогательный метод для изменения текущего выбранного элемента.
        """
        if (self.DeviceList.count() > 1):
            print(self.DeviceList.count(), self.DeviceList.selectedItems())
            self.idx = self.DeviceList.row(self.DeviceList.selectedItems()[0])
        else:
            self.idx = -1
        
    def new_connection(self):
        """
        Создание нового объекта Device, отображение его метки в списке и т.д.
        """
        name, done = QtWidgets.QInputDialog.getText(self, 'Device Name', 'Введите имя подключаемого устройства: ')
        if done or name != '':
            device = Device(name)
            device.build_connection()
            list_connection.append(device)
            self.DeviceList.addItem(device.name)

            with open('config/device_config.csv', mode='a') as f: # добавление записи в файл настроек
                f.write(name + ',0,defpath\n')

    def open_settings(self):
        """
        Вызов окна настроек для выбранного в QListWidget устройства
        """
        print("open settings for", list_connection[self.idx].name, "...")
        list_connection[self.idx].open_settings(name=list_connection[self.idx].name)


    def delete_connection(self):
        """
        Вызов метода завершения сессии, удаление объекта Device, соответствующему выбранному устройству
        """
        if (self.DeviceList.count() > 0):
            if (self.DeviceList.count() - 1 < self.idx):
                self.idx = self.DeviceList.count() - 1
            list_connection[self.idx].close_connection()
            self.DeviceList.takeItem(self.idx)
            list_connection.pop(self.idx)

def main():
    app = QtWidgets.QApplication(sys.argv)  
    window = ExampleApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()