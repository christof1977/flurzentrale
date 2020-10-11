#!/usr/bin/env python3

from os import path, getenv

import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QDate, QTime, QDateTime, Qt, pyqtSignal, pyqtSlot
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
from libby import remote




OekofenWindowUI, OekofenWindowBase = loadUiType(path.join(path.dirname(path.abspath(__file__)), 'gui/oekofenwindow.ui'))


class OekofenWindow(OekofenWindowBase, OekofenWindowUI):

    statusSignal = pyqtSignal('QString') # erstelle Signal, um Status in Mainwindiw zu aktualisieren

    def __init__(self, parent):
        super(OekofenWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButtonHome.clicked.connect(self.home)
        self.readConfig()
        self.tStop = threading.Event()
        self.updateOekofen()


    def readConfig(self):
        try:
            configfile = path.join(path.dirname(path.abspath(__file__)), 'config.ini')
            self.config = configparser.ConfigParser()
            self.config.read(configfile)
            self.pelle = self.config['BASE']['Pelle']
        except:
            print("Configuration error")




    def home(self):
        #self.hide()
        self.tStop.set()
        self.close()

    def _updateOekofen(self):
        while(not self.tStop.is_set()):
            try:
                json_string = '{"command" : "getOekofendata"}'
                d = remote.udpRemote(json_string, addr="dose", port=6663)
                self.lbl_pe1_status.setText(str(d["pe1"]["L_statetext"]))
                self.lbl_pe1_modulation.setText(str(d["pe1"]["L_modulation"])+"%")
                self.lbl_pe1_temp_act.setText(str(float(d["pe1"]["L_temp_act"])/10)+" °C")
                self.lbl_pe1_avg_runtime.setText(str(float(d["pe1"]["L_avg_runtime"]))+" min")
                self.lbl_hk1_flowtemp_set.setText(str(float(d["hk1"]["L_flowtemp_set"])/10)+" °C")
                self.lbl_hk1_flowtemp_act.setText(str(float(d["hk1"]["L_flowtemp_act"])/10)+" °C")
                self.lbl_pu1_tpo_act.setText(str(float(d["pu1"]["L_tpo_act"])/10)+" °C")
                self.lbl_pu1_tpm_act.setText(str(float(d["pu1"]["L_tpm_act"])/10)+" °C")
                self.lbl_sk1_spu.setText(str(float(d["sk1"]["L_spu"])/10)+" °C")
                self.lbl_sk1_koll_temp.setText(str(float(d["sk1"]["L_koll_temp"])/10)+" °C")
                self.lbl_sk1_pump.setText(str(d["sk1"]["L_pump"])+" %")
                self.lbl_sk3_koll_temp.setText(str(float(d["sk3"]["L_koll_temp"])/10)+" °C")
                self.lbl_sk3_pump.setText(str(d["sk3"]["L_pump"])+" %")
                self.lbl_se2_flow_temp.setText(str(float(d["se2"]["L_flow_temp"])/10)+" °C")
                self.lbl_se2_ret_temp.setText(str(float(d["se2"]["L_ret_temp"])/10)+" °C")
                self.lbl_se2_day.setText(str(float(d["se2"]["L_day"])/10)+" kWh")
                self.lbl_se2_yesterday.setText(str(float(d["se2"]["L_yesterday"])/10)+" kWh")
                st_fill = str(d["pe1"]["L_storage_fill"]) + " kg"
                st_popper = str(d["pe1"]["L_storage_popper"]) + " kg"
                self.lbl_pe1_storage_fill.setText(st_fill)
                self.lbl_pe1_storage_popper.setText(st_popper)

            except Exception as e:
                self.statusSignal.emit("Fehler "+ str(e))
                print(str(e))
            self.tStop.wait(11)

    def updateOekofen(self):
        oekoT = threading.Thread(target=self._updateOekofen)
        oekoT.setDaemon(True)
        oekoT.start()


def main():
    pass

if __name__ == "__main__":
    main()
