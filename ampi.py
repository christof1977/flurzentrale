#!/usr/bin/env python3

from os import path, getenv

import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

import subprocess

import threading
from threading import Thread
import socket
import time
import sys
import syslog
import datetime
import json
from kodijson import Kodi
from libby import remoteAmpiUdp


AmpiWindowUI, AmpiWindowBase = loadUiType(path.join(path.dirname(path.abspath(__file__)), 'gui/ampiwindow.ui'))


class AmpiWindow(AmpiWindowBase, AmpiWindowUI):

    statusSignal = pyqtSignal('QString') # erstelle Signal, um Status in Mainwindow zu aktualisieren


    def __init__(self, parent):
        self.status = 0
        if(type(parent) is not list):
            self.ampiConfig = parent.radioConfig
            super(AmpiWindow, self).__init__(parent)
        else:
            self.ampiConfig = parent
            super(AmpiWindow, self).__init__()
        self.setupUi(self) # gets defined in the UI file
        #self.pushButtonRadioStop.clicked.connect(self.stopRadio)
        #self.pushButtonRadioPlay.clicked.connect(self.playRadio)
        self.pushButtonVolDown.clicked.connect(self.volDown)
        self.pushButtonVolUp.clicked.connect(self.volUp)
        self.pushButtonMute.clicked.connect(self.mute)
        self.pushButtonHome.clicked.connect(self.home)
        self.pushButtonCD.clicked.connect(self.cd)
        self.pushButtonLP.clicked.connect(self.lp)
        self.pushButtonPi.clicked.connect(self.pi)
        self.pushButtonPortable.clicked.connect(self.portable)
        self.pushButtonCassette.clicked.connect(self.cassette)
        self.pushButtonSchneitzlberger.clicked.connect(self.schneitzlberger)
        self.pushButtonClock.clicked.connect(self.clock)
        self.pushButtonLight.clicked.connect(self.light)



    def checkStatus(self):
        #print(self.status)
        if(self.status):
            self.home()


    def volUp(self):
        remoteAmpiUdp.sende(None, self.ampiConfig[2], self.ampiConfig[3], "vol_up")
        self.statusSignal.emit("Lauter")

    def volDown(self):
        remoteAmpiUdp.sende(None, self.ampiConfig[2], self.ampiConfig[3], "vol_down")
        self.statusSignal.emit("Leiser")

    def mute(self):
        remoteAmpiUdp.sende(None, self.ampiConfig[2], self.ampiConfig[3], "mute")
        self.statusSignal.emit("Still")

    def schneitzlberger(self):
        remoteAmpiUdp.sende(None, self.ampiConfig[2], self.ampiConfig[3], "Schneitzlberger")
        self.statusSignal.emit("Schneitzlberger")

    def cd(self):
        remoteAmpiUdp.sende(None, self.ampiConfig[2], self.ampiConfig[3], "CD")
        self.statusSignal.emit("CD")

    def lp(self):
        remoteAmpiUdp.sende(None, self.ampiConfig[2], self.ampiConfig[3], "Bladdnspiela")
        self.statusSignal.emit("Bladdnspiela")

    def pi(self):
        remoteAmpiUdp.sende(None, self.ampiConfig[2], self.ampiConfig[3], "Himbeer314")
        self.statusSignal.emit("Himbeer314")

    def portable(self):
        remoteAmpiUdp.sende(None, self.ampiConfig[2], self.ampiConfig[3], "Portable")
        self.statusSignal.emit("Portable")

    def cassette(self):
        remoteAmpiUdp.sende(None, self.ampiConfig[2], self.ampiConfig[3], "Hilfssherriffeingang")
        self.statusSignal.emit("Hilfssherriffeingang")

    def clock(self):
        remoteAmpiUdp.sende(None, self.ampiConfig[2], self.ampiConfig[3], "dim_sw")
        self.statusSignal.emit("LCD an oder aus")

    def light(self):
        remoteAmpiUdp.sende(None, self.ampiConfig[2], self.ampiConfig[3], "hyperion")
        self.statusSignal.emit("Lichtspiele")



    def home(self):
        self.hide()



def main():
    import platform
    node = platform._syscmd_uname('-n')
    os = platform._syscmd_uname('')
    machine = platform.machine()
    app = QApplication(sys.argv)
    radioConfigW  = ["Wohnzimmer", "osmd.fritz.box", "osmd.fritz.box", 5005]
    anzeige = AmpiWindow(radioConfigW)
    if(node == "flur" and os == "Linux"):
        anzeige.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        anzeige.move(0, 0)
    anzeige.show()
    #app.exec_()
    sys.exit(app.exec_())
    #sys.exit()

if __name__ == "__main__":
    main()
