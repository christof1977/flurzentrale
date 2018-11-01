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
        self.ampiConfig = parent.radioConfig
        super(AmpiWindow, self).__init__(parent)
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



    def checkStatus(self):
        #print(self.status)
        if(self.status):
            self.home()


    def volUp(self):
        if(self.ampiConfig[2]!=None):
            remoteAmpiUdp.sende(None, self.ampiConfig[2], self.ampiConfig[3], "vol_up")
            self.statusSignal.emit("Lauter")

    def volDown(self):
        if(self.ampiConfig[2]!=None):
            remoteAmpiUdp.sende(None, self.ampiConfig[2], self.ampiConfig[3], "vol_down")
            self.statusSignal.emit("Leiser")

    def mute(self):
        pass

    def cd(self):
        pass

    def lp(self):
        pass

    def pi(self):
        pass


    def home(self):
        self.hide()
        #self.close()



