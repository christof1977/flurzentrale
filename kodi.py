#!/usr/bin/env python3

from os import path, getenv

import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt, pyqtSignal, pyqtSlot, QSize, QStringListModel
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
from libby import remoteAmpi

from stations import radioStations


KodiWindowUI, KodiWindowBase = loadUiType(path.join(path.dirname(path.abspath(__file__)), 'gui/kodiwindow.ui'))


class KodiWindow(KodiWindowBase, KodiWindowUI):

    statusSignal = pyqtSignal('QString') # erstelle Signal, um Status in Mainwindow zu aktualisieren


    def __init__(self, parent):
        self.status = 0
        self.radioConfig = parent.radioConfig
        super(KodiWindow, self).__init__(parent)
        self.setupUi(self) # gets defined in the UI file
        self.pushButtonRadioStop.clicked.connect(self.stopKodi)
        self.pushButtonVolDown.clicked.connect(lambda: self.changeVolume("Down"))
        self.pushButtonVolUp.clicked.connect(lambda: self.changeVolume("Up"))
        self.pushButtonHome.clicked.connect(self.home)
        self.startKodi(parent)



    def startKodi(self, parent):
        p = subprocess.Popen(['ping',self.radioConfig[1],'-c','1',"-W","2"])
        p.wait()
        if(p.poll() == 0): #Hier gehts weiter, wenn ping erfolgreich war
            try:
                self.kodi = Kodi("http://"+self.radioConfig[1]+"/jsonrpc")
                print(self.kodi.JSONRPC.Ping())
                self.labelTitle.setText("Kodi "+self.radioConfig[0])
                self.artists = self.kodi.AudioLibrary.GetArtists()
                self.artists = self.artists['result']
                artistList = []
                for key in self.artists['artists']:
                    artistList.append(key['artist'])
                    QListWidgetItem(key['artist'], self.lwArtist)

            except:
                print("Kein Kodi da!")
                self.labelTitle.setText("Fehler: "+self.radioConfig[0])
                #time.sleep(1)
                self.statusSignal.emit("Nix Radio!")
                self.status = 1
        else: # Hier lang ohne erfolgreichen ping
            print("nix is!")
            self.statusSignal.emit("Nix Kodi!")
            self.status = 1
        model = QStringListModel()
        model.setStringList(artistList)
        completer = QCompleter()
        completer.setModel(model)
        self.leArtist.setCompleter(completer)


    def checkStatus(self):
        #print(self.status)
        if(self.status):
            self.home()

    def changeKodiVolume(self, par):
        try:
            ret = "Ups ..."
            if(par == "Up"):
                ret = self.kodi.Application.SetVolume({"volume": "increment"})['result']
            elif(par == "Down"):
                ret = self.kodi.Application.SetVolume({"volume": "decrement"})['result']
            if(par == "Mute"):
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
        remoteAmpi.udpRemote(json_cmd, addr=self.radioConfig[2], port=self.radioConfig[3])
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

    def stopKodi(self):
        if(self.radioConfig[2] is not None):
            print("mit Verstärker")
            #self.send2ampi("Input", "Schneitzlberger")
        try:
            playerid=self.kodi.Player.GetActivePlayers()["result"][0]["playerid"]
            result = self.kodi.Player.Stop({"playerid": playerid})
            self.statusSignal.emit("Aus is!")
        except:
            pass

    def home(self):
        self.hide()
        #self.close()



