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
from heizung import HeizungWindow
#from kodi import KodiWindow

import threading
from threading import Thread
import socket
import time
import sys
import syslog
import datetime
import json
import select
from kodijson import Kodi

from libby.remote import udpRemote

import resources_rc

garagn_tcp_addr = 'garagn.home'
garagn_tcp_port = 80

buffer_size = 1024
radioConfigW  = ["Wohnzimmer", "osmd.home", "osmd", 5005]
radioConfigA  = ["Arbeitszimmmer", "osme.home", None, None]

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.dirname(path.abspath(__file__))
        #base_path = os.path.abspath(".")

    return path.join(base_path, relative_path)

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

    def udpRx(self):
        self.udpRxTstop = threading.Event()
        rxValT = threading.Thread(target=self._udpRx)
        rxValT.setDaemon(True)
        rxValT.start()

    def _udpRx(self):
        port =  6664
        print("Starting UDP client on port ", port)
        udpclient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, \
                socket.IPPROTO_UDP)  # UDP
        udpclient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        udpclient.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        udpclient.bind(("", port))
        udpclient.setblocking(0)
        while(not self.udpRxTstop.is_set()):
            ready = select.select([udpclient], [], [], .1)
            if ready[0]:
                data, addr = udpclient.recvfrom(8192)
                try:
                    message = json.loads(data.decode())
                    if("measurement" in message.keys()):
                        meas = message["measurement"]
                        for key in meas:
                            self.display_rx_value(key, meas[key])
                except Exception as e:
                    print(str(e))

    def display_rx_value(self, key, message):
        if(key == "tempFlur"):
            self.labelWzTemp.setText("{} {}".format(round(message["Value"],1), message["Unit"]))
        elif(key == "humFlur"):
            self.labelWzHum.setText("{} {}".format(round(message["Value"],1), message["Unit"]))
        elif(key == "pressFlur"):
            self.labelWzPress.setText("{} {}".format(round(message["Value"],1), message["Unit"]))
        elif(key == "tempOekoAussen"):
            self.labelTempDraussen1.setText("{} {}".format(round(message["Value"],1), message["Unit"]))
        elif(key == "AussenKuecheTemp"):
            self.labelTempDraussen2.setText("{} {}".format(round(message["Value"],1), message["Unit"]))
        elif(key == "Garagentor"):
            if(message['Value'] == "auf"):
                self.pushButtonTor.setIcon(QtGui.QIcon(":/images/gui/garage_open.png"))
            elif(message['Value'] == "zu"):
                self.pushButtonTor.setIcon(QtGui.QIcon(":/images/gui/garage_closed.png"))



    def _uhr(self):
        counter = 0
        while(not self.t_stop.is_set()):
            now=datetime.datetime.now()
            if self.uhrzeitdp == 1:
                uhrzeit="{0:0>2}".format(now.hour)+" "+"{0:0>2}".format(now.minute)
                self.uhrzeitdp = 0
            else:
                uhrzeit="{0:0>2}".format(now.hour)+":"+"{0:0>2}".format(now.minute)
                self.uhrzeitdp = 1
            # Reset labelStatus if text display for 3 seconds:
            if(self.labelStatusTime <= 2):
                self.labelStatusTime += 1
            else:
                self.labelStatus.setText("Dumdidum ...")
            self.labelTime.setText(uhrzeit)
            self.labelDate.setText(str(now.day).zfill(2)+'.'+str(now.month).zfill(2)+'.'+str(now.year))
            #self.update_torstatus()
            self.t_stop.wait(1)

    def uhr(self):
        self.labelStatusTime = 3
        self.uhrzeitdp = 1
        self.schaunach = 0
        uhrTh = threading.Thread(target=self._uhr)
        uhrTh.setDaemon(True)
        uhrTh.start()

    def torAufZu(self):
        json_cmd = '{"command" : "setTor" , "Request":"auf"}\n'
        self.labelStatus.setText("Warte kurz")
        ret = udpRemote(json_cmd, addr="piesler", port=5005)

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

    def openHeizung(self):
        self.heizung =  HeizungWindow(self)
        self.heizung.statusSignal.connect(self.setStatus)
        self.heizung.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.heizung.move(0, 0)
        self.heizung.show()
        self.heizung.raise_()
        self.heizung.checkStatus()


    def __init__(self):

        super(self.__class__, self).__init__()
        self.setupUi(self) # gets defined in the UI file

        self.pushButtonTor.clicked.connect(self.torAufZu)
        self.pushButtonOpenRadioW.clicked.connect(self.openRadioW)
        self.pushButtonOpenRadioA.clicked.connect(self.openRadioA)
        self.pushButtonOpenAmpi.clicked.connect(self.openAmpi)
        self.pushButtonOpenOekofen.clicked.connect(self.openOekofen)
        self.pushButtonOpenHeizung.clicked.connect(self.openHeizung)
        #self.pushButtonOpenKodi.clicked.connect(self.openKodi)


        self.t_stop = threading.Event()

        self.uhr()
        self.udpRx()

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
