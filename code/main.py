from PyQt5.QtWidgets import QApplication

from MainWindow import *



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()