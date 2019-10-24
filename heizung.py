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

    def get_btn_obj(self, room):
        ret = -1
        for i in range(self.gridLayoutUnten.count()):
            btn = self.gridLayoutUnten.itemAt(i).widget()
            if(btn.objectName() == room):
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
            print(name)
            if(key == "shorttimer"):
                room = name[1]
                if(self.status[room]["ShorttimerMode"] == "run"):
                    text = self.status[room]["Shorttimer"]
                else:
                    text = ""
                self.gridLayoutUnten.itemAt(i).widget().setText(str(text))
        for room in self.status:
            pass

    def init_screen(self):
        self.gridLayoutUnten.setContentsMargins(5, 5, 5, 5)
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
            for position, room in zip(line_positions, self.hz[self.floor]["rooms"]):
                self.create_btn(room, position)
                text = self.status[room]["isTemp"]
                self.create_lbl(room, "isTemp", text, tuple(map(sum, zip((0,1), position))))
                self.create_lbl(room, "shorttimer", text, tuple(map(sum, zip((0,2), position))))



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
                self.update_btns()
                self.update_lbls()
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
