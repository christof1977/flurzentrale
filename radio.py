#!/usr/bin/env python3

from os import path, getenv
import time

import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

#from gui.radiowindow_ui import Ui_RadioWindow
#import radiowindow


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

#osmd  = "http://osmd.fritz.box/jsonrpc"
#ampi = "osmd.fritz.box"
#ampiPort = 5005




def sende(tcp_sock, tcp_addr, tcp_port, json_cmd):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((tcp_addr, tcp_port))
        s.send(json_cmd.encode())
        data = s.recv(buffer_size, socket.MSG_WAITALL)
        return data.decode()
        s.close()
    except Exception as e:
        #print("Verbinungsfehler")
        return '{"Aktion" : "Fehler", "Parameter" : "Verbindung"}\n'

def json_dec(json_string):
    try:
        out = json.loads(json_string)
    except:
        json_string = '{"Aktion" : "Fehler", "Parameter" : "JSON"}\n'
        out = json.loads(json_string)
        #print("Json-Fehler")
    return out

RadioWindowUI, RadioWindowBase = loadUiType(path.join(path.dirname(path.abspath(__file__)), 'gui/radiowindow.ui'))


class RadioWindow(RadioWindowBase, RadioWindowUI):

    def __init__(self, parent):
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
        #print(self.radioConfig[0])
        #self.kodi = Kodi(osmd)
        try:
            self.kodi = Kodi(self.radioConfig[1])
            print(self.kodi.JSONRPC.Ping())
            self.labelTitle.setText("Radio "+self.radioConfig[0])
        except:
            print("Kein Kodi da!")
            self.labelTitle.setText("Fehler: "+self.radioConfig[0])
            time.sleep(1)
            parent.labelStatus.setText("Ups ...")

    def playRadio(self):
        if(self.radioConfig[2]!=None):
            remoteAmpiUdp.sende(None, ampi, ampiPort, "Himbeer314")
        radio2play = self.listWidgetRadio.currentItem().text()
        try:
            radioUrl = radioStations[radio2play]
        except:
            print("No URL found!")
        try:
            ret = self.kodi.Player.Open({"item": {"file": radioUrl}})
            #print(ret)
            print("Starting", radioUrl)
        except Exception as e:
            print("Could not start radio!", radioUrl)
            #print(str(e))

    def stopRadio(self):
        if(self.radioConfig[2]!=None):
            print("mit Verstärker")
            remoteAmpiUdp.sende(None, ampi, ampiPort, "Schneitzlberger")
        try:
            playerid=self.kodi.Player.GetActivePlayers()["result"][0]["playerid"]
            result = self.kodi.Player.Stop({"playerid": playerid})
        except:
            pass

    def volUp(self):
        if(self.radioConfig[2]!=None):
            remoteAmpiUdp.sende(None, ampi, ampiPort, "vol_up")

    def volDown(self):
        if(self.radioConfig[2]!=None):
            remoteAmpiUdp.sende(None, ampi, ampiPort, "vol_down")

    def home(self):
        self.hide()
        self.close()



