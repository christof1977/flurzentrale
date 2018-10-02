#!/usr/bin/env python3

# From https://www.baldengineer.com/raspberry-pi-gui-tutorial.html 
# by James Lewis (@baldengineer)
# Minimal python code to start PyQt5 GUI

import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt
from PyQt5.QtWidgets import *
from mainwindow import Ui_MainWindow
import mainwindow

from radiowindow import Ui_RadioWindow
import radiowindow


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

#import mysql.connector
from libby import mysqldose
from libby.mysqldose import mysqldose

garagn_tcp_addr = 'garagn.fritz.box'
garagn_tcp_port = 80
buffer_size = 1024
osmd  = "http://osmd.fritz.box/jsonrpc"
ampi = "osmd.fritz.box"
ampiPort = 5005


radioUrls = ["http://webstream.gong971.de/gong971",
             "http://nbg.starfm.de/player/pls/nbg_pls_mp3.php.pls",
             "http://www.antenne.de/webradio/antenne.m3u",
             "http://www.rockantenne.de/webradio/rockantenne.aac.pls"
             ]
radioNames = ["Radio Gong",
              "StarFM",
              "Antenne Bayern",
              "Rock Antenne",
              "Rock Antenne",
              "Rock Antenne",
              "Rock Antenne"
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


class MainWindow(QMainWindow, Ui_MainWindow):
# access variables inside of the UI's file

### functions for the buttons to call
#def pressedOnButton(self):
#    print ("Pressed On!")

    def hole_temp_db(self):
        pass
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
            self.labelTime.setText(uhrzeit)
            self.labelDate.setText(str(now.day)+'.'+str(now.month)+'.'+str(now.year))
            self.update_torstatus()
            self.update_temp()
            self.t_stop.wait(1)


    def uhr(self):
        self.uhrzeitdp = 1
        self.schaunach = 0 
        self.holetemp = 0
        threading.Thread(target=self._uhr).start()

    def pushButtonTorClicked(self):
        #time.sleep(.5)
        json_cmd = '{"Aktion" : "Kommando", "Parameter" : "TorAufZu"}\n'
        self.labelStatus.setText("Warte kurz")
        data = sende(1, garagn_tcp_addr, garagn_tcp_port, json_cmd)
        status = json.loads(data)
        if(status['Aktion'] == "Antwort" and status['Parameter'] == "OK"):
            self.labelStatus.setText("Bassd")
        else:
            self.labelStatus.setText("Ups ...")

    def openRadio(self):
        self.radio =  RadioWindow(self)
        self.radio.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.radio.move(0, 0)
        self.radio.show()


    def __init__(self):
        self.mysqluser = 'heizung'
        self.mysqlpass = 'heizung'
        self.mysqlserv = 'dose.fritz.box'
        self.mysqldb   = 'heizung'
        super(self.__class__, self).__init__()
        self.setupUi(self) # gets defined in the UI file

#        self.pushButtonTor.clicked.connect(self.pushButtonTorClicked)
        self.pushButtonOpenRadio.clicked.connect(self.openRadio)

        self.t_stop = threading.Event()

        self.uhr()
        self.operate = 0
        self.db = mysqldose(self.mysqluser, self.mysqlpass, self.mysqlserv, self.mysqldb)
        #self.mysql_success = False
        self.db.start()
        self.hole_temp_db()


class RadioWindow(QMainWindow, Ui_RadioWindow):


    def defineRadioList(self):
        for radioName in radioNames:
            item = QtWidgets.QListWidgetItem(radioName)
            font = QtGui.QFont()
            font.setPointSize(24)
            item.setFont(font)
            brush = QtGui.QBrush(QtGui.QColor(162, 162, 162))
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

def main():
    app = QApplication(sys.argv)
    anzeige = MainWindow()
    anzeige.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    anzeige.move(0, 0)
    anzeige.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 
