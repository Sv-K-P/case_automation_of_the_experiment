#defSettingsWindow.py

from PyQt5 import QtWidgets

from qtdesign.settings_window import Ui_SettingsWindow

class ExampleSet(QtWidgets.QMainWindow, Ui_SettingsWindow):
    """
    Класс для инициализации окна с настройками устройства
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)