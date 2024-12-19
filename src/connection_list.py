# connection_list.py

from defSettingsWindow import ExampleSet

class Device():
    """
    :brief Класс для описания подключенных устройств.

    Операции с устройствами, такие как настройка начальных параметров, получение значений
    производятся через объекты этого класса

    :todo добавить методы инициализации, коммутации с устройством
    """
    def __init__(self, name: str) -> None:
        self.name = name

    def open_settings(self, name):
        """
        Вызов окна с настройками

        :bug При нажатии кнопки с пустым QListWidget
        """
        self.window_settings = ExampleSet(name=name)
        self.window_settings.show()
    
    def build_connection(self):
        """
        Установка подключения с камерой
        """
        pass

    def close_connection(self):
        """
        Завершение связи с камерой
        """
        pass