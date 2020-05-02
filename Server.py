from PyQt5.QtWidgets import QApplication
from ServerGUI import Ui_MainWindow
from threading import Thread


if __name__ == '__main__':
    app = QApplication([])
    ServerGUI = Ui_MainWindow()
    ServerGUI.show()
    # GUIThread = Thread(target=app.exec)
    app.exec()