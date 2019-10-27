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
import calendar
import locale


#from libby import remote
from libby.remote import udpRemote


RoomDetailWindowUI,RoomDetailWindowBase = loadUiType(path.join(path.dirname(path.abspath(__file__)), 'gui/detailwindow.ui'))


class RoomDetailWindow(RoomDetailWindowBase, RoomDetailWindowUI):

    statusSignal = pyqtSignal('QString') # erstelle Signal, um Status in Mainwindow zu aktualisieren

    def __init__(self, parent, room):
        super(RoomDetailWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButtonHome.clicked.connect(self.home)
        self.host = parent.hz[parent.floor]["host"]
        self.status = parent.status[room]
        self.labelTitle.setText(self.status["Name"])
        self.tStop = threading.Event()
        self.timer = self.get_timer(room)
        self.init_screen()

    def get_timer(self, room):
        cmd = {"command":"getTimer", "Room":room}
        ans= udpRemote(json.dumps(cmd), addr=self.host, port=5005)
        return(ans)

    def checkStatus(self):
        #print(self.stat)
        if(self.stat):
            self.home()

    def home(self):
        #self.hide()
        self.tStop.set()
        self.close()

    def create_lbl(self, text, row, col):
        lbl = QLabel()
        #lbl.setObjectName(text)
        lbl.setText(str(text))
        lbl.setStyleSheet("QLabel {color: white;}")
        self.gridLayoutUnten.addWidget(lbl, row, col)

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
        locale.setlocale(locale.LC_ALL, 'de_DE')
        days = list(calendar.day_name)
        j = 0
        for day in self.timer:
            self.create_lbl(days[int(day)], j, 0)
            i = 0
            for time in self.timer[day][0]:
                self.create_lbl(time + " -> " + self.timer[day][1][i], j, i+1)
                i += 1
            j += 1
            #for time in self.timer[day]:
                #print(time)

def main():
    pass

if __name__ == "__main__":
    main()
