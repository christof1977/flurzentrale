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
from libby.remote import udpRemote


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
        self.pushButtonVolDown.clicked.connect(lambda: self.send2ampi("Volume", "Down"))
        self.pushButtonVolUp.clicked.connect(lambda: self.send2ampi("Volume", "Up"))
        self.pushButtonMute.clicked.connect(lambda: self.send2ampi("Volume", "Mute"))
        self.pushButtonHome.clicked.connect(self.home)
        self.pushButtonCD.clicked.connect(lambda: self.send2ampi("Input", "CD"))
        self.pushButtonLP.clicked.connect(lambda: self.send2ampi("Input", "Bladdnspiela"))
        self.pushButtonPi.clicked.connect(lambda: self.send2ampi("Input", "Himbeer314"))
        self.pushButtonPortable.clicked.connect(lambda: self.send2ampi("Input", "Portable"))
        self.pushButtonCassette.clicked.connect(lambda: self.send2ampi("Input", "Hilfssherriff"))
        self.pushButtonSchneitzlberger.clicked.connect(lambda: self.send2ampi("Input", "Schneitzlberger"))
        self.pushButtonPower.clicked.connect(lambda: self.send2ampi("Switch", "Power"))
        self.pushButtonClock.clicked.connect(lambda: self.send2ampi("Switch", "DimOled"))
        self.pushButtonLight.clicked.connect(lambda: self.send2ampi("Hyperion", ""))



    def checkStatus(self):
        if(self.status):
            self.home()

    def send2ampi(self, aktion, par):
        cmd = { "Aktion": aktion, "Parameter": par }
        json_cmd = json.dumps(cmd)
        ret = udpRemote(json_cmd, addr=self.ampiConfig[2], port=self.ampiConfig[3])
        if(ret != -1):
            ret = (json.loads(ret))
            for key in ret.items():
                print(key)
            self.statusSignal.emit(ret['Antwort'] + ": " + par)

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
