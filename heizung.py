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

    def create_btn(self, floor, room, position):
        print("Create btn", floor, room)
        btn = QPushButton()
        btn.setObjectName(room)
        btn.setText(room)
        btn.setStyleSheet('QPushButton {color: white; border-style: solid; height: 15px; width: 60px; border-width: 1px; border-color: grey;}')
        self.gridLayoutUnten.addWidget(btn, *position)
        btn.clicked.connect(lambda: self.btn_click(room))
        self.set_button(room)

    def set_btn_active(self, room):
        btn = self.get_btn_obj(room)
        btn.setStyleSheet('QPushButton {color: white; border-style: solid; height: 15px; width: 60px; border-width: 1px; border-color: grey; background-color: green}')

    def set_btn_inactive(self, room):
        btn = self.get_btn_obj(room)
        btn.setStyleSheet('QPushButton {color: white; border-style: solid; height: 15px; width: 60px; border-width: 1px; border-color: grey;}')

    def get_btn_obj(self, room):
        ret = -1
        for i in range(self.gridLayoutUnten.count()):
            btn = self.gridLayoutUnten.itemAt(i).widget()
            if(btn.objectName() == room):
                ret = btn
        return(ret)

    def set_button(self, room):
        btn = self.get_btn_obj(room)
        print(btn)
        if(btn != -1):
            if(self.status[room]["Status"] == "on"):
                self.set_btn_active(room)
                #btn.setStyleSheet('QPushButton {background-color: green;} ')
                #print("on")
            else:
                self.set_btn_inactive(room)
                #btn.setStyleSheet('QPushButton {background-color: black;} ')

    def update_btns(self):
        old_status = self.status
        self.status = udpRemote('{"command" : "getStatus"}', addr=self.hz[self.floor]["host"], port=5005)
        for room in self.status:
            if(self.status[room]["Status"] != old_status[room]["Status"]):
                if(self.status[room]["Status"] == "on"):
                    self.set_btn_active(room)
                else:
                    self.set_btn_inactive(room)
        pass


    def init_screen(self):
        self.gridLayoutUnten.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutUnten.setObjectName("gridLayoutUnten")
        while(self.gridLayoutUnten.count() > 0):
            item = self.gridLayoutUnten.takeAt(0)
            if not item:
                continue
            w = item.widget()
            if w:
                w.deleteLater()
        positions = [(i,j) for i in range(3) for j in range(5)]
        if(udpRemote('{"command" : "getAlive"}', addr=self.hz[self.floor]["host"], port=5005)["answer"] == "Freilich"):
            self.status = udpRemote('{"command" : "getStatus"}', addr=self.hz[self.floor]["host"], port=5005)
            self.hz[self.floor]["rooms"] = []
            for room in self.status:
                self.hz[self.floor]["rooms"].append(room)
            for position, room in zip(positions, self.hz[self.floor]["rooms"]):
                #print(position, room)
                self.create_btn(self.floor, room, position)


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
                self.update_btns()
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
