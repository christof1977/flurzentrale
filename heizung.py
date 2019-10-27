#!/usr/bin/env python3

from os import path, getenv

import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt, pyqtSignal, pyqtSlot, QSize
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from PyQt5.QtGui import QIcon, QPixmap

import subprocess

import threading
from threading import Thread
import socket
import time
import sys
import syslog
import datetime
import json
import urllib
import urllib.request
import configparser

#from libby import remote
from libby.remote import udpRemote


HeizungWindowUI, HeizungWindowBase = loadUiType(path.join(path.dirname(path.abspath(__file__)), 'gui/heatingwindow.ui'))


class HeizungWindow(HeizungWindowBase, HeizungWindowUI):

    statusSignal = pyqtSignal('QString') # erstelle Signal, um Status in Mainwindow zu aktualisieren

    def __init__(self, parent):
        super(HeizungWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButtonHome.clicked.connect(self.home)
        self.pushButtonDg.clicked.connect(self.selectDg)
        self.pushButtonEg.clicked.connect(self.selectEg)
        self.hz = {}
        self.hz["EG"] = {}
        self.hz["DG"] = {}
        self.floor = "EG"
        self.readConfig()
        self.tStop = threading.Event()
        self.ping_controller()
        self.init_screen()
        self.update()

    def ping_controller(self):
        p = subprocess.Popen(['ping',self.hz[self.floor]["host"],'-c','1',"-W","2"])
        p.wait()
        self.stat = 1
        if(p.poll() == 0): #Hier gehts weiter, wenn ping erfolgreich war
            self.stat = 0
            return()
        else: # Hier lang ohne erfolgreichen ping
            self.statusSignal.emit("Keine Antwort")
            self.stat = 1
            print("nix is!")

    def checkStatus(self):
        #print(self.stat)
        if(self.stat):
            self.home()

    def get_btn_obj(self, name):
        ret = -1
        for i in range(self.gridLayoutUnten.count()):
            btn = self.gridLayoutUnten.itemAt(i).widget()
            if(btn.objectName() == name):
                ret = btn
        return(ret)

    def create_room(self, room, line):
        btnStyleSheet = ("QPushButton {" +
                                      "color: rgb(255, 255, 255);" +
                                      "background-color: rgb(0, 0,0);" +
                                      "border-color: rgb(40, 40, 40);" +
                                      "border-radius: 4px;" +
                                     "} " +
                          "QPushButton:pressed {" +
                                       "background-color: rgb(60,60,60)" +
                                      "}")
        #print("Building Screen")
        font = QtGui.QFont(".SF NS Text", 12)
        # Display Room Name (first column)
        #lbl = QLabel()
        #lbl.setObjectName(room + "_name")
        #lbl.setText(str(self.status[room]["Name"]))
        #lbl.setStyleSheet("QLabel {color: white;}")
        #lbl.setFont(font)
        #self.gridLayoutUnten.addWidget(lbl, line, 0)
        btn = QPushButton()
        btn.setObjectName(room + "_name")
        btn.setText(str(self.status[room]["Name"]))
        btn.setStyleSheet(btnStyleSheet)
        btn.setMinimumSize(32,32)
        self.gridLayoutUnten.addWidget(btn, line, 0)
        # Display Power Icon (second column)
        btn = QPushButton()
        btn.setObjectName(room + "_pwrBtn")
        btn.setIcon(QIcon(":/images/gui/power.png"))
        btn.setStyleSheet(btnStyleSheet)
        btn.setIconSize(QSize(32,32))
        btn.setMinimumSize(32,32)
        self.gridLayoutUnten.addWidget(btn, line, 1)
        #btn.clicked.connect(lambda: self.btn_click(room))
        # Display Thermometer (third column)
        btn = QPushButton()
        btn.setObjectName(room + "_thermBtn")
        btn.setIcon(QIcon(":/images/gui/thermometer_small.png"))
        btn.setIconSize(QSize(32,32))
        btn.setMinimumSize(32,32)
        self.gridLayoutUnten.addWidget(btn, line, 2)
        # Display measured temperature (fourth column)
        lbl = QLabel()
        lbl.setObjectName(room + "_temp")
        lbl.setText(str(self.status[room]["isTemp"])+"°C")
        lbl.setFont(font)
        lbl.setStyleSheet("QLabel {color: white;}")
        self.gridLayoutUnten.addWidget(lbl, line, 3)
        # Display On timer (5th column)
        btn = QPushButton()
        btn.setObjectName(room + "_onTmrBtn")
        btn.setIcon(QIcon(":/images/gui/timer_green.png"))
        btn.setStyleSheet(btnStyleSheet)
        btn.setIconSize(QSize(32,32))
        btn.setMinimumSize(32,32)
        self.gridLayoutUnten.addWidget(btn, line, 4)
        btn.clicked.connect(lambda: self.set_shorttimer(room, "on"))
        # Display Off timer (6th column)
        btn = QPushButton()
        btn.setObjectName(room + "_offTmrBtn")
        btn.setIcon(QIcon(":/images/gui/timer_red.png"))
        btn.setStyleSheet(btnStyleSheet)
        btn.setIconSize(QSize(32,32))
        btn.setMinimumSize(32,32)
        self.gridLayoutUnten.addWidget(btn, line, 5)
        btn.clicked.connect(lambda: self.set_shorttimer(room, "off"))
        # Display remaining time (7th column)
        lbl = QLabel()
        lbl.setObjectName(room + "_shorttimer")
        if(self.status[room]["ShorttimerMode"] == "run"):
            text = str(self.status[room]["Shorttimer"])+"s"
        else:
            text = ""
        lbl.setFont(font)
        lbl.setText(text)
        lbl.setStyleSheet("QLabel {color: white;}")
        self.gridLayoutUnten.addWidget(lbl, line, 6)


    def update_room(self, room):
        #print("Updating",room)
        #if(self.status[room]["Status"] != self.old_status[room]["Status"]):
        if True:
            if(self.status[room]["Status"] == "on"):
                #print("on")
                self.set_pwrBtn_on(room)
            else:
                #print("off")
                self.set_pwrBtn_off(room)

    def set_pwrBtn_off(self, room):
        btn = self.get_btn_obj(room + "_pwrBtn")
        btn.setIcon(QIcon(":/images/gui/power.png"))

    def set_pwrBtn_on(self, room):
        btn = self.get_btn_obj(room + "_pwrBtn")
        btn.setIcon(QIcon(":/images/gui/power_green.png"))

    def init_screen(self):
        self.gridLayoutUnten.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutUnten.setHorizontalSpacing(10)
        self.gridLayoutUnten.setObjectName("gridLayoutUnten")
        # Delete all widgets in Layout, if existing (cleaning layout)
        while(self.gridLayoutUnten.count() > 0):
            item = self.gridLayoutUnten.takeAt(0)
            if not item:
                continue
            w = item.widget()
            if w:
                w.deleteLater()
        line_positions = [(i,j) for i in range(5) for j in range(1)]
        ans= udpRemote('{"command" : "getAlive"}', addr=self.hz[self.floor]["host"], port=5005)
        print(ans)
        if(ans == -1):
            print("Mist")
            self.statusSignal.emit("Keine Antwort")
            self.home()
            return(-1)
        alive = ans["answer"]
        if(alive == "Freilich"):
            #self.status = udpRemote('{"command" : "getStatus"}', addr=self.hz[self.floor]["host"], port=5005)
            self.get_status()
            self.hz[self.floor]["rooms"] = []
            for room in self.status:
                self.hz[self.floor]["rooms"].append(room)
            self.hz[self.floor]["rooms"] = sorted(self.hz[self.floor]["rooms"])
            i = 0
            for room in self.hz[self.floor]["rooms"]:
                self.create_room(room, i)
                i += 1
            self.update_status()
        return()

    def set_shorttimer(self, room, mode):
        self.get_status()
        if(self.status[room]["Mode"] == mode):
            print(cmd)
            print(room)
            print(mode)

    def selectEg(self):
        self.floor = "EG"
        #self.ping_controller()
        self.init_screen()
        print(self.floor)

    def selectDg(self):
        self.floor = "DG"
        self.init_screen()
        print(self.floor)

    def btn_click(self,room):
        status = udpRemote('{"command" : "getRoomStatus", "Room" : "' + room + '"}', addr=self.hz[self.floor]["host"], port=5005)
        if(status["status"]["Status"] == "off"):
            cmd = '{"command" : "setRoomShortTimer", "Room" : "' + room + '", "Mode": "on" ,"Time" : "900" }'
            ans = udpRemote(cmd, addr=self.hz[self.floor]["host"], port=5005)
            self.statusSignal.emit(room + " an")
            print(ans)
        else:
            cmd = '{"command" : "setRoomShortTimer", "Room" : "' + room + '", "Mode": "off" ,"Time" : "900" }'
            ans = udpRemote(cmd, addr=self.hz[self.floor]["host"], port=5005)
            self.statusSignal.emit(room + " aus")

    def readConfig(self):
        try:
            configfile = path.join(path.dirname(path.abspath(__file__)), 'config.ini')
            self.config = configparser.ConfigParser()
            self.config.read(configfile)
            self.hz["DG"]["host"] = self.config['BASE']['HeizungDG']
            self.hz["EG"]["host"] = self.config['BASE']['HeizungEG']
        except:
            print("Configuration error")

    def home(self):
        #self.hide()
        self.tStop.set()
        self.close()

    def get_status(self):
        self.status = udpRemote('{"command" : "getStatus"}', addr=self.hz[self.floor]["host"], port=5005)

    def update_status(self):
        self.old_status = self.status
        self.get_status()
        #print("update")
        for room in self.hz[self.floor]["rooms"]:
            self.update_room(room)

    def _update(self):
        while(not self.tStop.is_set()):
            try:
                self.update_status()
            except Exception as e:
                self.statusSignal.emit("Fehler "+ str(e))
                print(str(e))
            self.tStop.wait(5)

    def update(self):
        updateT = threading.Thread(target=self._update)
        updateT.setDaemon(True)
        updateT.start()


def main():
    pass

if __name__ == "__main__":
    main()