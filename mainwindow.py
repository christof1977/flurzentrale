# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(480, 320)
        MainWindow.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.labelTime = QtWidgets.QLabel(self.centralWidget)
        self.labelTime.setGeometry(QtCore.QRect(160, 290, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.labelTime.setFont(font)
        self.labelTime.setStyleSheet("color: rgb(255, 255, 255);")
        self.labelTime.setObjectName("labelTime")
        self.labelDate = QtWidgets.QLabel(self.centralWidget)
        self.labelDate.setGeometry(QtCore.QRect(10, 290, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.labelDate.setFont(font)
        self.labelDate.setStyleSheet("color: rgb(255, 255, 255);")
        self.labelDate.setObjectName("labelDate")
        self.labelStatus = QtWidgets.QLabel(self.centralWidget)
        self.labelStatus.setGeometry(QtCore.QRect(370, 290, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.labelStatus.setFont(font)
        self.labelStatus.setStyleSheet("color: rgb(255, 255, 255);")
        self.labelStatus.setObjectName("labelStatus")
        self.pushButtonOpenRadio = QtWidgets.QPushButton(self.centralWidget)
        self.pushButtonOpenRadio.setGeometry(QtCore.QRect(330, 220, 141, 51))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.pushButtonOpenRadio.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.pushButtonOpenRadio.setFont(font)
        self.pushButtonOpenRadio.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.pushButtonOpenRadio.setStyleSheet("QPushButton\n"
"{\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 0,0);\n"
"border-color: rgb(40, 40, 40);\n"
"border-width: 3px;        \n"
"border-style: solid;\n"
"border-radius: 4px;\n"
"}\n"
"QPushButton:pressed\n"
"{\n"
"background-color: rgb(40,40,40)\n"
"}\n"
"")
        self.pushButtonOpenRadio.setObjectName("pushButtonOpenRadio")
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.labelTime.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt;\">25:25:61</span></p></body></html>"))
        self.labelDate.setText(_translate("MainWindow", "32.13.2018"))
        self.labelStatus.setText(_translate("MainWindow", "Öhäm ..."))
        self.pushButtonOpenRadio.setText(_translate("MainWindow", "Radio"))

