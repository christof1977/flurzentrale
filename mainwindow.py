# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.9
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
        self.labelTime.setGeometry(QtCore.QRect(30, 290, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.labelTime.setFont(font)
        self.labelTime.setStyleSheet("color: rgb(255, 255, 255);")
        self.labelTime.setObjectName("labelTime")
        self.labelDate = QtWidgets.QLabel(self.centralWidget)
        self.labelDate.setGeometry(QtCore.QRect(180, 290, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.labelDate.setFont(font)
        self.labelDate.setStyleSheet("color: rgb(255, 255, 255);")
        self.labelDate.setObjectName("labelDate")
        self.tabWigdet = QtWidgets.QTabWidget(self.centralWidget)
        self.tabWigdet.setGeometry(QtCore.QRect(0, 0, 480, 281))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.tabWigdet.setFont(font)
        self.tabWigdet.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tabWigdet.setAccessibleName("")
        self.tabWigdet.setAccessibleDescription("")
        self.tabWigdet.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWigdet.setAutoFillBackground(False)
        self.tabWigdet.setStyleSheet("QTabBar::tab { height: 40px; width: 150px; }\n"
"/*QTabBar::tab:text\n"
"{\n"
"    border-top-color: #1D2A32;\n"
"    border-color: #40494E;\n"
"    color: white;\n"
"}*/\n"
"QTabBar::tab\n"
"{\n"
"    color: white;\n"
"    background-color: black;\n"
"    border-color: grey;\n"
"    border-bottom-color: black; /* same as pane color */\n"
"}\n"
"QTabBar::tab:selected\n"
"{ \n"
"    background-color: rgb(40, 40, 40);\n"
"}")
        self.tabWigdet.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWigdet.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWigdet.setIconSize(QtCore.QSize(16, 16))
        self.tabWigdet.setUsesScrollButtons(False)
        self.tabWigdet.setTabBarAutoHide(False)
        self.tabWigdet.setObjectName("tabWigdet")
        self.tabEg = QtWidgets.QWidget()
        self.tabEg.setEnabled(True)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.tabEg.setFont(font)
        self.tabEg.setObjectName("tabEg")
        self.labelTab1Temp1 = QtWidgets.QLabel(self.tabEg)
        self.labelTab1Temp1.setGeometry(QtCore.QRect(50, 60, 151, 51))
        self.labelTab1Temp1.setStyleSheet("font: 48pt \".SF NS Text\";\n"
"color: rgb(255, 255, 255);")
        self.labelTab1Temp1.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTab1Temp1.setObjectName("labelTab1Temp1")
        self.labelTab1Temp2 = QtWidgets.QLabel(self.tabEg)
        self.labelTab1Temp2.setGeometry(QtCore.QRect(260, 60, 151, 51))
        self.labelTab1Temp2.setStyleSheet("font: 48pt \".SF NS Text\";\n"
"color: rgb(255, 255, 255);")
        self.labelTab1Temp2.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTab1Temp2.setObjectName("labelTab1Temp2")
        self.labelTab1Temp3 = QtWidgets.QLabel(self.tabEg)
        self.labelTab1Temp3.setGeometry(QtCore.QRect(50, 160, 151, 51))
        self.labelTab1Temp3.setStyleSheet("font: 48pt \".SF NS Text\";\n"
"color: rgb(255, 255, 255);")
        self.labelTab1Temp3.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTab1Temp3.setObjectName("labelTab1Temp3")
        self.labelTab1Temp4 = QtWidgets.QLabel(self.tabEg)
        self.labelTab1Temp4.setGeometry(QtCore.QRect(260, 160, 151, 51))
        self.labelTab1Temp4.setStyleSheet("font: 48pt \".SF NS Text\";\n"
"color: rgb(255, 255, 255);")
        self.labelTab1Temp4.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTab1Temp4.setObjectName("labelTab1Temp4")
        self.labelTab1Temp1Label = QtWidgets.QLabel(self.tabEg)
        self.labelTab1Temp1Label.setGeometry(QtCore.QRect(80, 30, 81, 16))
        self.labelTab1Temp1Label.setStyleSheet("color: rgb(255, 255, 255);")
        self.labelTab1Temp1Label.setObjectName("labelTab1Temp1Label")
        self.labelTab1Temp2Label = QtWidgets.QLabel(self.tabEg)
        self.labelTab1Temp2Label.setGeometry(QtCore.QRect(300, 30, 91, 16))
        self.labelTab1Temp2Label.setStyleSheet("color: rgb(255, 255, 255);")
        self.labelTab1Temp2Label.setObjectName("labelTab1Temp2Label")
        self.labelTab1Temp3Label = QtWidgets.QLabel(self.tabEg)
        self.labelTab1Temp3Label.setGeometry(QtCore.QRect(100, 140, 31, 16))
        self.labelTab1Temp3Label.setStyleSheet("color: rgb(255, 255, 255);")
        self.labelTab1Temp3Label.setObjectName("labelTab1Temp3Label")
        self.labelTab1Temp4Label = QtWidgets.QLabel(self.tabEg)
        self.labelTab1Temp4Label.setGeometry(QtCore.QRect(300, 140, 60, 16))
        self.labelTab1Temp4Label.setStyleSheet("color: rgb(255, 255, 255);")
        self.labelTab1Temp4Label.setObjectName("labelTab1Temp4Label")
        self.tabWigdet.addTab(self.tabEg, "")
        self.tabDg = QtWidgets.QWidget()
        self.tabDg.setObjectName("tabDg")
        self.tabWigdet.addTab(self.tabDg, "")
        self.tabGarage = QtWidgets.QWidget()
        self.tabGarage.setObjectName("tabGarage")
        self.pushButtonTor = QtWidgets.QPushButton(self.tabGarage)
        self.pushButtonTor.setGeometry(QtCore.QRect(120, 50, 240, 60))
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
        self.pushButtonTor.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(25)
        self.pushButtonTor.setFont(font)
        self.pushButtonTor.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        self.pushButtonTor.setStyleSheet("QPushButton\n"
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
        self.pushButtonTor.setObjectName("pushButtonTor")
        self.labelTorstatus = QtWidgets.QLabel(self.tabGarage)
        self.labelTorstatus.setGeometry(QtCore.QRect(110, 130, 261, 61))
        font = QtGui.QFont()
        font.setPointSize(40)
        self.labelTorstatus.setFont(font)
        self.labelTorstatus.setStyleSheet("color: rgb(255, 0, 0);")
        self.labelTorstatus.setAlignment(QtCore.Qt.AlignCenter)
        self.labelTorstatus.setObjectName("labelTorstatus")
        self.tabWigdet.addTab(self.tabGarage, "")
        self.labelStatus = QtWidgets.QLabel(self.centralWidget)
        self.labelStatus.setGeometry(QtCore.QRect(370, 290, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.labelStatus.setFont(font)
        self.labelStatus.setStyleSheet("color: rgb(255, 255, 255);")
        self.labelStatus.setObjectName("labelStatus")
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        self.tabWigdet.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.labelTime.setText(_translate("MainWindow", "25:25:61"))
        self.labelDate.setText(_translate("MainWindow", "32.13.2018"))
        self.labelTab1Temp1.setText(_translate("MainWindow", "99.9°C"))
        self.labelTab1Temp2.setText(_translate("MainWindow", "99.9°C"))
        self.labelTab1Temp3.setText(_translate("MainWindow", "99.9°C"))
        self.labelTab1Temp4.setText(_translate("MainWindow", "99.9°C"))
        self.labelTab1Temp1Label.setText(_translate("MainWindow", "Wohnzimmer"))
        self.labelTab1Temp2Label.setText(_translate("MainWindow", "Arbeitszimmer"))
        self.labelTab1Temp3Label.setText(_translate("MainWindow", "Bad"))
        self.labelTab1Temp4Label.setText(_translate("MainWindow", "Terrasse"))
        self.tabWigdet.setTabText(self.tabWigdet.indexOf(self.tabEg), _translate("MainWindow", "Temp EG"))
        self.tabWigdet.setTabText(self.tabWigdet.indexOf(self.tabDg), _translate("MainWindow", "Temp DG"))
        self.pushButtonTor.setText(_translate("MainWindow", "Tor"))
        self.labelTorstatus.setText(_translate("MainWindow", "Tor ist offen!"))
        self.tabWigdet.setTabText(self.tabWigdet.indexOf(self.tabGarage), _translate("MainWindow", "Garage"))
        self.labelStatus.setText(_translate("MainWindow", "Ups ..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

