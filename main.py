#!/usr/bin/env python3


from os import path, getenv

import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

from radio import RadioWindow
from ampi import AmpiWindow
from oekofen import OekofenWindow
from kodi import KodiWindow

import threading
from threading import Thread
import socket
import time
import sys
import syslog
import datetime
import json
from kodijson import Kodi

from libby import mysqldose
from libby.mysqldose import mysqldose

import resources_rc

garagn_tcp_addr = 'garagn.fritz.box'
garagn_tcp_port = 80
buffer_size = 1024
radioConfigW  = ["Wohnzimmer", "osmd.fritz.box", "osmd.fritz.box", 5005]
radioConfigA  = ["Arbeitszimmmer", "osme.fritz.box", None, None]

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.dirname(path.abspath(__file__))
        #base_path = os.path.abspath(".")

    return path.join(base_path, relative_path)


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


#MainWindowUI, MainWindowBase = loadUiType(path.join(path.dirname(path.abspath(__file__)), 'gui/mainwindow.ui'))
MainWindowUI, MainWindowBase = loadUiType(resource_path('gui/mainwindow.ui'))


class MainWindow(MainWindowBase, MainWindowUI):

    @pyqtSlot('QString')
    def setStatus(self, msg):
        self.labelStatusTime = 0
        self.labelStatus.setText(msg)

    def hole_temp_db(self):
        self.labelTempDraussen.setText(str(self.db.read_one("OekoAussenTemp"))+"°C")
#        self.labelTab1Temp1.setText(str(self.db.read_one("WohnzimmerTemp"))+"°C")
#        self.labelTab1Temp2.setText(str(self.db.read_one("ArbeitszimmerTemp"))+"°C")
#        self.labelTab1Temp3.setText(str("--- °C"))
#        self.labelTab1Temp4.setText(str(self.db.read_one("TerrasseTemp"))+"°C")

#        self.labelTab2Temp1.setText(str(self.db.read_one("LeahTemp"))+"°C")
#        self.labelTab2Temp2.setText(str(self.db.read_one("FelixTemp"))+"°C")
#        self.labelTab2Temp3.setText(str(self.db.read_one("BadDGTemp"))+"°C")
#        self.labelTab2Temp4.setText(str("--- °C"))

#        self.labelTab4Temp1.setText(str(round(self.db.read_one("kVorlauf"),1))+"°C")
#        self.labelTab4Temp2.setText(str(round(self.db.read_one("kRuecklauf"),1))+"°C")
#        self.labelTab4Temp3.setText(str(round(self.db.read_one("ntVorlaufDGTemp"),1))+"°C")
#        self.labelTab4Temp4.setText(str(round(self.db.read_one("ntRuecklaufDGTemp"),1))+"°C")

    def update_temp(self):
        if(self.holetemp <= 5):
            self.holetemp += 1
        else:
            self.hole_temp_db()
            self.holetemp = 0


    def update_torstatus(self):
        if(self.schaunach == 5):
            json_cmd = '{"Aktion" : "Abfrage", "Parameter" : "Torstatus"}\n'
            data = sende(1, garagn_tcp_addr, garagn_tcp_port, json_cmd)
            #status = json.loads(data)
            status = json_dec(data)
            if(status['Aktion'] == "Antwort" and status['Parameter'] == "Auf"):
                self.labelTorstatus.setText("Tor ist offen!")
                self.labelTorstatus.setStyleSheet('color: red')
            elif(status['Aktion'] == "Antwort" and status['Parameter'] == "Zu"):
                self.labelTorstatus.setText("Tor ist zu.")
                self.labelTorstatus.setStyleSheet('color: green')
            self.schaunach = 0
        else:
            self.schaunach += 1

    def _uhr(self):
        while(not self.t_stop.is_set()):
            now=datetime.datetime.now()
            if self.uhrzeitdp == 1:
                #uhrzeit=str(now.hour)+" "+str(now.minute)
                uhrzeit="{0:0>2}".format(now.hour)+" "+"{0:0>2}".format(now.minute)
                self.uhrzeitdp = 0
            else:
                #uhrzeit=str(now.hour)+":"+str(now.minute)
                uhrzeit="{0:0>2}".format(now.hour)+":"+"{0:0>2}".format(now.minute)
                self.uhrzeitdp = 1

            # Reset labelStatus if text display for 3 seconds:
            if(self.labelStatusTime <= 2):
                self.labelStatusTime += 1
            else:
                self.labelStatus.setText("Dumdidum ...")

            self.labelTime.setText(uhrzeit)
            self.labelDate.setText(str(now.day).zfill(2)+'.'+str(now.month).zfill(2)+'.'+str(now.year))
            self.update_torstatus()
            self.update_temp()
            self.t_stop.wait(1)


    def uhr(self):
        self.labelStatusTime = 3
        self.uhrzeitdp = 1
        self.schaunach = 0
        self.holetemp = 0
        uhrTh = threading.Thread(target=self._uhr)
        uhrTh.setDaemon(True)
        uhrTh.start()

    def torAufZu(self):
        print("Tor")
        #time.sleep(.5)
        json_cmd = '{"Aktion" : "Kommando", "Parameter" : "TorAufZu"}\n'
        self.labelStatus.setText("Warte kurz")
        data = sende(1, garagn_tcp_addr, garagn_tcp_port, json_cmd)
        status = json.loads(data)
        if(status['Aktion'] == "Antwort" and status['Parameter'] == "OK"):
            self.labelStatus.setText("Bassd")
        else:
            self.labelStatus.setText("Ups ...")

    def openRadioA(self):
        self.radioConfig = radioConfigA
        self.openRadio()

    def openRadioW(self):
        self.radioConfig = radioConfigW
        self.openRadio()

    def openRadio(self):
        self.radio =  RadioWindow(self)
        self.radio.statusSignal.connect(self.setStatus)
        self.radio.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.radio.move(0, 0)
        self.radio.show()
        self.radio.raise_()
        self.radio.checkStatus()

    def openAmpi(self):
        self.radioConfig = radioConfigW
        self.ampi =  AmpiWindow(self)
        self.ampi.statusSignal.connect(self.setStatus)
        self.ampi.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.ampi.move(0, 0)
        self.ampi.show()
        self.ampi.raise_()

    def openKodi(self):
        self.radioConfig = radioConfigW
        self.kodi =  KodiWindow(self)
        self.kodi.statusSignal.connect(self.setStatus)
        self.kodi.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.kodi.move(0, 0)
        self.kodi.show()
        self.kodi.raise_()


    def openOekofen(self):
        self.oekofen =  OekofenWindow(self)
        self.oekofen.statusSignal.connect(self.setStatus)
        self.oekofen.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.oekofen.move(0, 0)
        self.oekofen.show()
        self.oekofen.raise_()


    def __init__(self):
        self.mysqluser = 'heizung'
        self.mysqlpass = 'heizung'
        self.mysqlserv = 'dose.fritz.box'
        self.mysqldb   = 'heizung'
        super(self.__class__, self).__init__()
        self.setupUi(self) # gets defined in the UI file

        self.pushButtonTor.clicked.connect(self.torAufZu)
        self.pushButtonOpenRadioW.clicked.connect(self.openRadioW)
        self.pushButtonOpenRadioA.clicked.connect(self.openRadioA)
        self.pushButtonOpenAmpi.clicked.connect(self.openAmpi)
        self.pushButtonOpenOekofen.clicked.connect(self.openOekofen)
        self.pushButtonOpenKodi.clicked.connect(self.openKodi)


        self.t_stop = threading.Event()

        self.uhr()
        self.operate = 0
        self.db = mysqldose(self.mysqluser, self.mysqlpass, self.mysqlserv, self.mysqldb)
        #self.mysql_success = False
        self.db.start()
        self.hole_temp_db()



def main():
    import platform
    node = platform._syscmd_uname('-n')
    os = platform._syscmd_uname('')
    machine = platform.machine()
    app = QApplication(sys.argv)
    anzeige = MainWindow()
    if(node == "flur" and os == "Linux"):
        anzeige.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        anzeige.move(0, 0)
    anzeige.show()
    anzeige.raise_()
    app.exec_()
    #sys.exit(app.exec_())
    #sys.exit()

if __name__ == "__main__":
    main()
