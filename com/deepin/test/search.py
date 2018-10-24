# -*- coding: utf-8 -*-

# Form implementation generated from reading designer file 'search.designer'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!
import sqlite3
from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("MainWindow")
        mainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 10, 801, 121))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(30, 60, 72, 15))
        self.label.setObjectName("label")
        self.idInput = QtWidgets.QTextEdit(self.groupBox)
        self.idInput.setGeometry(QtCore.QRect(110, 50, 681, 31))
        self.idInput.setObjectName("id")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(0, 140, 801, 421))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(30, 30, 72, 15))
        self.label_2.setObjectName("label_2")
        self.address = QtWidgets.QTextEdit(self.groupBox_2)
        self.address.setGeometry(QtCore.QRect(110, 20, 681, 31))
        self.address.setObjectName("address")
        self.searchButton = QtWidgets.QPushButton(self.groupBox_2)
        self.searchButton.setGeometry(QtCore.QRect(320, 210, 93, 28))
        self.searchButton.setObjectName("searchButton")
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 25))
        self.menubar.setObjectName("menubar")
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(mainWindow)
        self.searchButton.clicked.connect(self.getAddress)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Id:"))
        self.label_2.setText(_translate("MainWindow", "Address:"))
        self.searchButton.setText(_translate("MainWindow", "GO"))

    def getAddress(self):
        # self.address.setText("hello")
        idInput = self.idInput.toPlainText()
        print(idInput)
        conn = sqlite3.connect('C:/sqlite/test.db')
        c = conn.cursor()
        print("Opened database successfully")
        cursor = c.execute("SELECT id, name, address, salary  from COMPANY WHERE id='{}'".format(idInput))
        address = "查无结果"
        try:
            for row in cursor:
                address = row[2]
        except Exception as err:
            print(err)
        finally:
            conn.close()

        self.address.setText(address)
