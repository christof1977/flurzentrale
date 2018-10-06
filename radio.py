#!/usr/bin/env python3


import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
from PyQt5.QtWidgets import *

from gui.radiowindow_ui import Ui_RadioWindow
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


osmd  = "http://osmd.fritz.box/jsonrpc"
ampi = "osmd.fritz.box"
ampiPort = 5005


radioUrls = ["http://webstream.gong971.de/gong971",
             "http://nbg.starfm.de/player/pls/nbg_pls_mp3.php.pls",
             "http://www.antenne.de/webradio/antenne.m3u",
             "http://www.rockantenne.de/webradio/rockantenne.aac.pls",
             "http://dg-br-http-fra-dtag-cdn.cast.addradio.de/br/br1/franken/mp3/128/stream.mp3?ar-distributor=f0a0",
             "http://dg-br-http-fra-dtag-cdn.cast.addradio.de/br/br2/nord/mp3/128/stream.mp3?ar-distributor=f0a0",
             "http://dg-br-http-fra-dtag-cdn.cast.addradio.de/br/brheimat/live/mp3/128/stream.mp3?ar-distributor=f0a0",
             "http://8.38.78.173:8210/stream/1/",
             "http://streaming.radio.co/saed08c46d/listen",
             "http://webradio.radiof.de:8000/radiof"
             ]
radioNames = ["Radio Gong",
              "StarFM",
              "Antenne Bayern",
              "Rock Antenne",
              "Bayern 1",
              "Bayern 2",
              "BR Heimat",
              "Audiophile Jazz",
              "Radio BUH",
              "Jazztime Nürnberg"
              ]



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



class RadioWindow(QMainWindow, Ui_RadioWindow):

    def __init__(self, parent):
        super(RadioWindow, self).__init__(parent)
        self.setupUi(self) # gets defined in the UI file
        self.pushButtonRadioStop.clicked.connect(self.stopRadio)
        self.pushButtonRadioPlay.clicked.connect(self.playRadio)
        self.pushButtonVolDown.clicked.connect(self.volDown)
        self.pushButtonVolUp.clicked.connect(self.volUp)
        self.pushButtonHome.clicked.connect(self.home)
        self.defineRadioList()
        self.startRadio()


    def defineRadioList(self):
        for radioName in radioNames:
            item = QtWidgets.QListWidgetItem(radioName)
            font = QtGui.QFont()
            font.setPointSize(24)
            item.setFont(font)
            brush = QtGui.QBrush(QtGui.QColor(160, 160, 160))
            brush.setStyle(QtCore.Qt.NoBrush)
            item.setForeground(brush)
            self.listWidgetRadio.addItem(item)
        self.listWidgetRadio.setCurrentRow(0)

    def startRadio(self):
        self.kodi = Kodi(osmd)
        pass

    def playRadio(self):
        remoteAmpiUdp.sende(None, ampi, ampiPort, "Himbeer314")
        radio2play = self.listWidgetRadio.currentItem().text()
        try:
            radioUrl = radioUrls[radioNames.index(radio2play)]
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
        remoteAmpiUdp.sende(None, ampi, ampiPort, "Schneitzlberger")
        try:
            playerid=self.kodi.Player.GetActivePlayers()["result"][0]["playerid"]
            result = self.kodi.Player.Stop({"playerid": playerid})
        except:
            pass

    def volUp(self):
        remoteAmpiUdp.sende(None, ampi, ampiPort, "vol_up")

    def volDown(self):
        remoteAmpiUdp.sende(None, ampi, ampiPort, "vol_down")

    def home(self):
        self.hide()
        #self.close()



