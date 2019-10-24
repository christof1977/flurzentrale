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
        self.init_screen()
        self.update()

    def create_btn(self, room, position):
        print("Create btn", room)
        btn = QPushButton()
        btn.setObjectName(room)
        btn.setText(room)
        self.gridLayoutUnten.addWidget(btn, *position)
        btn.clicked.connect(lambda: self.btn_click(room))
        self.set_button(room)

    def set_btn_active(self, room):
        btn = self.get_btn_obj(room)
        btn.setStyleSheet("QPushButton {color: white; border-style: solid; height: 25px; width: 60px; border-width: 1px; border-color: grey; background-color: green}")

    def set_btn_inactive(self, room):
        btn = self.get_btn_obj(room)
        btn.setStyleSheet("QPushButton {color: white; border-style: solid; height: 25px; width: 60px; border-width: 1px; border-color: grey;}")

    def get_btn_obj(self, name):
        ret = -1
        for i in range(self.gridLayoutUnten.count()):
            btn = self.gridLayoutUnten.itemAt(i).widget()
            if(btn.objectName() == name):
                ret = btn
        return(ret)

    def set_button(self, room):
        btn = self.get_btn_obj(room)
        if(btn != -1):
            if(self.status[room]["Status"] == "on"):
                self.set_btn_active(room)
            else:
                self.set_btn_inactive(room)

    def update_btns(self):
        for room in self.status:
            if(self.status[room]["Status"] != self.old_status[room]["Status"]):
                if(self.status[room]["Status"] == "on"):
                    self.set_btn_active(room)
                else:
                    self.set_btn_inactive(room)

    def create_lbl(self, room, col, text, position):
        print(room, col, position)
        lbl = QLabel()
        lbl.setObjectName(col+"_"+room)
        lbl.setText(str(text))
        lbl.setStyleSheet("QLabel {color: white;}")
        self.gridLayoutUnten.addWidget(lbl, *position)


    def update_lbls(self):
        for i in range(self.gridLayoutUnten.count()):
            name = (self.gridLayoutUnten.itemAt(i).widget().objectName().split("_"))
            key = name[0]
            #print(name)
            if(key == "shorttimer"):
                room = name[1]
                if(self.status[room]["ShorttimerMode"] == "run"):
                    text = self.status[room]["Shorttimer"]
                else:
                    text = ""
                self.gridLayoutUnten.itemAt(i).widget().setText(str(text))
        for room in self.status:
            pass

    def create_room(self, room, line):
        font = QtGui.QFont(".SF NS Text", 12)
        # Display Room Name (first column)
        lbl = QLabel()
        lbl.setObjectName(room + "_name")
        lbl.setText(str(self.status[room]["Name"]))
        lbl.setStyleSheet("QLabel {color: white;}")
        lbl.setFont(font)
        self.gridLayoutUnten.addWidget(lbl, line, 0)
        # Display Power Icon (second column)
        btn = QPushButton()
        btn.setObjectName(room + "_pwrBtn")
        btn.setIcon(QIcon(":/images/gui/power.png"))
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
        btn.setIconSize(QSize(32,32))
        btn.setMinimumSize(32,32)
        self.gridLayoutUnten.addWidget(btn, line, 4)
        # Display Off timer (6th column)
        btn = QPushButton()
        btn.setObjectName(room + "_offTmrBtn")
        btn.setIcon(QIcon(":/images/gui/timer_red.png"))
        btn.setIconSize(QSize(32,32))
        btn.setMinimumSize(32,32)
        self.gridLayoutUnten.addWidget(btn, line, 5)
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

        pass


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
        while(self.gridLayoutUnten.count() > 0):
            item = self.gridLayoutUnten.takeAt(0)
            if not item:
                continue
            w = item.widget()
            if w:
                w.deleteLater()
        line_positions = [(i,j) for i in range(5) for j in range(1)]
        if(udpRemote('{"command" : "getAlive"}', addr=self.hz[self.floor]["host"], port=5005)["answer"] == "Freilich"):
            self.status = udpRemote('{"command" : "getStatus"}', addr=self.hz[self.floor]["host"], port=5005)
            self.hz[self.floor]["rooms"] = []
            for room in self.status:
                self.hz[self.floor]["rooms"].append(room)
            self.hz[self.floor]["rooms"] = sorted(self.hz[self.floor]["rooms"])
            #for position, room in zip(line_positions, self.hz[self.floor]["rooms"]):
            #    self.create_btn(room, position)
            #    text = self.status[room]["isTemp"]
            #    self.create_lbl(room, "isTemp", text, tuple(map(sum, zip((0,1), position))))
            #    self.create_lbl(room, "shorttimer", text, tuple(map(sum, zip((0,2), position))))
            i = 0
            for room in self.hz[self.floor]["rooms"]:
                self.create_room(room, i)
                i += 1



    def selectEg(self):
        self.floor = "EG"
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

    def _update(self):
        while(not self.tStop.is_set()):
            try:
                self.old_status = self.status
                self.status = udpRemote('{"command" : "getStatus"}', addr=self.hz[self.floor]["host"], port=5005)
                #self.update_btns()
                #self.update_lbls()
                for room in self.hz[self.floor]["rooms"]:
                    self.update_room(room)
                pass
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
