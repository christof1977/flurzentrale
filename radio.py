#!/usr/bin/env python3

from os import path, getenv

import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt, pyqtSignal, pyqtSlot, QSize
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
        self.pushButtonVolDown.clicked.connect(lambda: self.changeVolume("down"))
        self.pushButtonVolUp.clicked.connect(lambda: self.changeVolume("up"))
        self.pushButtonHome.clicked.connect(self.home)
        self.defineRadioLogos()
        self.startRadio(parent)



    def defineRadioLogos(self):
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        positions = [(i,j) for i in range(3) for j in range(5)]

        for position, radioStation in zip(positions, sorted(radioStations.items())):
            if radioStation[0] == '':
                continue
            if radioStation[1][1] == '':
                continue
            btn = QPushButton()
            btn.setObjectName(radioStation[0])
            self.gridLayout.addWidget(btn, *position)
            btn.setIcon(QtGui.QIcon(radioStation[1][1]))
            btn.setIconSize(QSize(64, 64))
            btn.clicked.connect(self.playRadio)


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
            print("nix is!")
            self.statusSignal.emit("Nix Radio!")
            self.status = 1

    def checkStatus(self):
        #print(self.status)
        if(self.status):
            self.home()

    def changeKodiVolume(self, par):
        try:
            ret = "Ups ..."
            if(par == "up"):
                ret = self.kodi.Application.SetVolume({"volume": "increment"})['result']
            elif(par == "down"):
                ret = self.kodi.Application.SetVolume({"volume": "decrement"})['result']
            if(par == "mute"):
                ret = self.kodi.Application.SetVolume({"mute": True})['result']
            self.statusSignal.emit("Volume: " + str(ret))
        except Exception as e:
            print("Kann nicht mit Kodi labern: " + str(e))



    def changeVolume(self, par):
        if(self.radioConfig[2] is not None):
            self.send2ampi("Volume", par)
        else:
            self.changeKodiVolume(par)

    def send2ampi(self, aktion, par):
        cmd = { "Aktion": aktion, "Parameter": par }
        json_cmd = json.dumps(cmd)
        remoteAmpiUdp.sende(None, self.radioConfig[2], self.radioConfig[3], json_cmd)
        self.statusSignal.emit(aktion + ": " + par)

    def playRadio(self):
        if(self.radioConfig[2] is not None):
            self.send2ampi("Input", "Himbeer314")
        radio2play = self.sender().objectName()
        print(radio2play)
        try:
            radioUrl = radioStations[radio2play][0]
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
        if(self.radioConfig[2] is not None):
            print("mit Verstärker")
            self.send2ampi("Input", "Schneitzlberger")
        try:
            playerid=self.kodi.Player.GetActivePlayers()["result"][0]["playerid"]
            result = self.kodi.Player.Stop({"playerid": playerid})
            self.statusSignal.emit("Aus is!")
        except:
            pass

    def home(self):
        self.hide()
        #self.close()



