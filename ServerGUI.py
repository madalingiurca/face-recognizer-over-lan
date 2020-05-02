from threading import Thread

from PyQt5.QtCore import QRect
from PyQt5 import QtCore
from PyQt5.QtWidgets import *

from ServerClass import Server


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi()
        self.SPThread = Thread(target=self.ServerPeer)

    def setupUi(self):
        if self.objectName():
            self.setObjectName(u"MainWindow")
        self.resize(500, 300)
        self.centralwidget = QWidget(self)
        self.centralwidget.setObjectName(u"centralwidget")

        self.conLabel = QLabel(self.centralwidget)
        self.conLabel.setObjectName("conLabel")
        self.conLabel.setText("CONNECTED")
        self.conLabel.setGeometry(QRect(10, 120, 113, 22))
        self.conLabel.setStyleSheet('QLabel#conLabel {color: green}')
        self.conLabel.hide()

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(60, 220, 93, 28))
        self.pushButton.setText("Start Server")
        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(250, 220, 93, 28))
        self.pushButton_2.setText("Stop Server")
        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName(u"tableView")
        self.tableWidget.setGeometry(QRect(130, 20, 341, 192))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.tableWidget.setAutoScroll(False)
        self.tableWidget.setSelectionMode(QAbstractItemView.NoSelection)
        self.tableWidget.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget.setHorizontalHeaderLabels(["connection", "person"])
        self.tableWidget.hide()
        self.ip = QLineEdit(self.centralwidget)
        self.ip.setObjectName(u"ip")
        self.ip.setText("localhost")
        self.ip.setGeometry(QRect(10, 30, 113, 22))
        self.port = QLineEdit(self.centralwidget)
        self.port.setText("8888")
        self.port.setObjectName(u"port")
        self.port.setGeometry(QRect(10, 70, 113, 22))
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName(u"statusbar")
        self.setStatusBar(self.statusbar)

        self.pushButton.clicked.connect(self.connect)
        self.pushButton_2.clicked.connect(self.stop)

    def connect(self):
        try:
            HOST = self.ip.text()
            PORT = int(self.port.text())
            self.serv = Server(HOST, PORT)
            self.serv.load_resources()
            self.conLabel.show()
            self.serv.start()
            QMessageBox.information(self, "Connected", "Server started on {}:{}".format(HOST, PORT))
            self.pushButton.setDisabled(True)
            self.tableWidget.show()
            self.SPThread.start()
            self.pushButton_2.setDisabled(False)
        except Exception as e:
            QMessageBox.warning(self, "Warning", str(e))

    def stop(self):
        # TODO button_2 stop server implement
        self.pushButton.setDisabled(False)
        self.pushButton_2.setDisabled(True)
        self.serv.stop()
        self.SPThread.join()
        self.SPThread = Thread(target=self.ServerPeer)

        pass

    def ServerPeer(self):
        threads = []
        i = 0
        while True:
            try:
                conn, addr = self.serv.sock.accept()
                threads.append(Thread(target=self.connection, args=(conn, addr, i)))
                threads[i].start()
                i += 1
                if self.pushButton.isEnabled():
                    print("here")
                    break
            except OSError:
                if self.pushButton.isEnabled():
                    break

    def connection(self, conn, addr, i):
        self.tableWidget.setRowCount(i + 1)
        self.tableWidget.setItem(i, 0, QTableWidgetItem(addr[0]))
        while (1):
            data = self.serv.handler(conn, addr)
            if data == 0:
                print("break", i)
                break
            self.tableWidget.setItem(i, 1, QTableWidgetItem(data))
            self.tableWidget.viewport().update()

        self.tableWidget.setRowCount(i)
