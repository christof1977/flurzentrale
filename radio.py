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

from stations import radioStations


RadioWindowUI, RadioWindowBase = loadUiType(path.join(path.dirname(path.abspath(__file__)), 'gui/radiowindow.ui'))


class RadioWindow(RadioWindowBase, RadioWindowUI):

    statusSignal = pyqtSignal('QString') # erstelle Signal, um Status in Mainwindiw zu aktualisieren


    def __init__(self, parent):
        self.status = 0
        self.radioConfig = parent.radioConfig
        super(RadioWindow, self).__init__(parent)
        self.setupUi(self) # gets defined in the UI file
        self.pushButtonRadioStop.clicked.connect(self.stopRadio)
        self.pushButtonRadioPlay.clicked.connect(self.playRadio)
        self.pushButtonVolDown.clicked.connect(self.volDown)
        self.pushButtonVolUp.clicked.connect(self.volUp)
        self.pushButtonHome.clicked.connect(self.home)
        self.defineRadioList()
        self.startRadio(parent)

    def defineRadioList(self):
        for radioName in radioStations:
            item = QtWidgets.QListWidgetItem(radioName)
            font = QtGui.QFont()
            font.setPointSize(24)
            item.setFont(font)
            brush = QtGui.QBrush(QtGui.QColor(160, 160, 160))
            brush.setStyle(QtCore.Qt.NoBrush)
            item.setForeground(brush)
            self.listWidgetRadio.addItem(item)
        self.listWidgetRadio.setCurrentRow(0)

    def startRadio(self, parent):
        p = subprocess.Popen(['ping',self.radioConfig[1],'-c','1',"-W","2"])
        p.wait()
        if(p.poll() == 0): #Hier gehts weiter, wenn ping erfolgreich war
            try:
                self.kodi = Kodi("http://"+self.radioConfig[1]+"/jsonrpc")
                print(self.kodi.JSONRPC.Ping())
                self.labelTitle.setText("Radio "+self.radioConfig[0])
            except:
                print("Kein Kodi da!")
                self.labelTitle.setText("Fehler: "+self.radioConfig[0])
                #time.sleep(1)
                self.statusSignal.emit("Nix Radio!")
                self.status = 1
        else: # Hier lang ohne erfolgreichen ping
            self.statusSignal.emit("Nix Radio!")
            self.status = 1

    def checkStatus(self):
        #print(self.status)
        if(self.status):
            self.home()

    def playRadio(self):
        #if(self.radioConfig[2] != None):
        #    remoteAmpiUdp.sende(None, self.radioConfig[2], self.radioConfig[3], "Himbeer314")
        radio2play = self.listWidgetRadio.currentItem().text()
        print(radio2play)
        try:
            radioUrl = radioStations[radio2play]
        except:
            print("No URL found!")
        print(radioUrl)
        try:
            ret = self.kodi.Player.Open({"item": {"file": radioUrl}})
            print("Starting", radioUrl)
            self.statusSignal.emit(radio2play)
        except Exception as e:
            print("Could not start radio!", radioUrl)
            #print(str(e))

    def stopRadio(self):
        if(self.radioConfig[2]!=None):
            print("mit Verstärker")
            remoteAmpiUdp.sende(None, self.radioConfig[2], self.radioConfig[3], "Schneitzlberger")
        try:
            playerid=self.kodi.Player.GetActivePlayers()["result"][0]["playerid"]
            result = self.kodi.Player.Stop({"playerid": playerid})
            self.statusSignal.emit("Aus is!")
        except:
            pass

    def volUp(self):
        if(self.radioConfig[2]!=None):
            remoteAmpiUdp.sende(None, self.radioConfig[2], self.radioConfig[3], "vol_up")
            self.statusSignal.emit("Lauter")

    def volDown(self):
        if(self.radioConfig[2]!=None):
            remoteAmpiUdp.sende(None, self.radioConfig[2], self.radioConfig[3], "vol_down")
            self.statusSignal.emit("Leiser")

    def home(self):
        self.hide()
        #self.close()



