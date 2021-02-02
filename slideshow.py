# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie
from PyQt5.Qt import Qt
import time
import sys
import os
import logging
import argparse
import json
from math import floor
from PIL import Image
from pprint import pprint

def def_params():
    parser = argparse.ArgumentParser(
            description=
            """
            Slideshow - odpowiada za wyświetlanie pobranych zdjęć

            Klawisze akcji:
            - spacja - przejście w tryb pełnoekranowy
            - escape - wyjście z trybu pełnoekranowego
            parametry do wyswietlenia:
            """
            )
    #UWAGA - nie dopisuj argumentom wartości default - do takich wartości używamy tylko i wyłącznie plik konfiguracyjny
    parser.add_argument("-l", "--debug_logslideshow", action='store_true', help="ustaw flage 'debug' i wyswietlaj logi")
    parser.add_argument("-s", "--sizeOfLoadingBar", help="ustaw rozmiar(grubość) loadingBara")
    parser.add_argument("-f", "--fullScreenSlideshow", action='store_true', help="ustaw maksymalny rozmiar programu przy odpaleniu programu")
    parser.add_argument("-t", "--timeForPicture", type=int, help="podaj czas w [s] dla każdego obrazka")
    parser.add_argument("-wd", "--workdirectory", help="argument wskazuje folder roboczy - wazny z tego wzgledu że tam powinien się znajdować plik konfiguracyjny")
    parser.add_argument("-mapa", "--mapapng", help="url do ścieszki z png screenshota mapy - uwaga zalecany format png!(jpg ma pewne problemy w walidacji)")
    parser.add_argument("-widget", "--widgetpng", help="url do ścieszki z png screenshota widgeta - uwaga zalecany format png!(jpg ma pewne problemy w walidacji)")
    parser.add_argument("-kwadrat", "--kwadratpng", help="url do ścieszki z png używanego w LoadingBar-ze - uwaga zalecany format png!")
    args = parser.parse_args()
    for key, value in list(args.__dict__.items()):
        if value is None or value == False:
            print(f"usuniete {key} {value}")
            del args.__dict__[key]
    print("after command line")
    pprint(args.__dict__)

    if os.path.exists('config.json'):
        config_args = argparse.Namespace()
        with open('config.json', 'rt') as f:
             config_args = argparse.Namespace()
             config_args.__dict__.update(json.load(f))
             pprint(config_args)
             config_args.__dict__.update(vars(args))
        for key, value in list(config_args.__dict__.items()):
            if value == "False" or value == "false":
                config_args.__dict__[key]=False
            elif value == "True" or value == "true":
                config_args.__dict__[key]=True
            if key == "__comment__":
                del config_args.__dict__[key]
    else:
        print("Brak pliku konfiguracyjnego - jeśli żadnego nie posiadasz prośba o skopiowanie \n config.json.example i nazwanie owej kopii config.json")

    if config_args.debug_logslideshow:
        logging.basicConfig(level=logging.DEBUG, force=True)
        logging.debug("Ten komunikat pokazuje sie tylko w trybie debug")
        print("config_args:")
        pprint(config_args.__dict__)
    return config_args

class Ui_MainWindow(object):

    def __init__(self, sizeOfLoadingBar, timeForPicture):
        logging.debug("UI_MainWindow __init__")
        self.lab_loadingbBar = None #label na loadingbara
        self.lab_MapOrWidget = None #label na widget/mape
        self.timerLoadingBar = None
        self.flagaWidget = 1 #flaga mowiaca czy jest teraz mapa czy widget
        self.widthWindow = 925
        self.heightWindow = 810
        self.sizeOfLoadingBar = int(sizeOfLoadingBar)
        self.czasObrazka = int(timeForPicture)*1000 #w milisekundach #bez int - napis zostanie ... wygenerowany 1000 razy
        self.timeToDownloadPictures = 60*1000
        self.MainWindow = None
        self.mapapng = mapa
        self.widgetpng = widget
        self.kwadratpng = kwadrat
        self.wypelnienie = 0

        #timery
        self.timerPicture = None #timerPicture do zamiany zdjęć
        self.timerDownloader = None
        self.timerLoadingBar = None
        self.initLog()

    def initLog(self):
        logging.debug("initLog")
        logging.debug("widthWindow: "+str(self.widthWindow))
        logging.debug("heightWindow: "+str(self.heightWindow))
        logging.debug("czasObrazka: "+str(self.czasObrazka))
        logging.debug("wypelnienie: "+str(self.wypelnienie))
        logging.debug(self.mapapng)
        logging.debug(self.widgetpng)
        logging.debug(self.kwadratpng)

    def setupUi(self, MainWindow):
        logging.debug("setupUi")
        #glówne okno
        self.mainWindow = MainWindow
        self.mainWindow.setObjectName("MainWindow")
        self.mainWindow.setWindowTitle("MainWindow")
        self.mainWindow.resize(self.widthWindow, self.heightWindow)
        #pasek u góry
        self.lab_loadingBar = QtWidgets.QLabel(self.mainWindow)
        self.setWidthLoadingBar()
        self.lab_loadingBar.setText("")
        self.lab_loadingBar.setScaledContents(True)
        self.lab_loadingBar.setObjectName("lab_loadingBar")
        self.lab_loadingBar.setPixmap(QtGui.QPixmap(self.kwadratpng))
        self.lab_loadingBar.setScaledContents(True)
        #mapa i widget
        self.lab_MapOrWidget = QtWidgets.QLabel(MainWindow)
        self.lab_MapOrWidget.setGeometry(QtCore.QRect(0, self.sizeOfLoadingBar, self.widthWindow, self.heightWindow-20))
        self.lab_MapOrWidget.setText("")
        self.lab_MapOrWidget.setPixmap(QtGui.QPixmap(self.mapapng))
        self.lab_MapOrWidget.setScaledContents(True)
        self.lab_MapOrWidget.setObjectName("lab_MapOrWidget")
        #timery
        self.setTimerDownloadPictures()
        self.setTimerChangePicture()
        self.setTimerLoadingBar()

    def setWidthLoadingBar(self):
        self.lab_loadingBar.setGeometry(QtCore.QRect(0,0, self.wypelnienie * self.widthWindow/10, self.sizeOfLoadingBar))

    #uwaga - metoda verify dziala tylko dla png formatu
    def checkPicture(self, picturepng):
        img = Image.open(picturepng)
        brokenImage=False
        try:
            img.verify()
            print(f"Poprawny png {picturepng}")
            brokenImage=False
        except Exception:
            brokenImage=True
            print('Błąd przy odczycie zdjęcia {picturepng}')
        return brokenImage


    def changePicture(self):
        logging.debug("changePicture Function - flagWidget="+str(self.flagaWidget))
        if self.flagaWidget == 0:
            brokenImage=self.checkPicture(self.mapapng)
            if brokenImage == False:
                self.lab_MapOrWidget.setPixmap(QtGui.QPixmap(self.mapapng))
            else:
                self.lab_MapOrWidget.setPixmap(QtGui.QPixmap(f'{self.mapapng}.bkp'))
                logging.debug(f'{self.mapapng}.bkp')
            self.flagaWidget = 1
            self.wypelnienie = 0
            self.setWidthLoadingBar()
        else:
            brokenImage=self.checkPicture(self.widgetpng)
            if brokenImage == False:
                self.lab_MapOrWidget.setPixmap(QtGui.QPixmap(self.widgetpng))
            else:
                self.lab_MapOrWidget.setPixmap(QtGui.QPixmap(f'{self.widgetpng}.bkp'))
                logging.debug(f'{self.widgetpng}.bkp')
            self.flagaWidget = 0
            self.wypelnienie = 0
            self.setWidthLoadingBar()

    def changeLoadingBar(self):
        if self.wypelnienie < 11:
            self.wypelnienie = self.wypelnienie+1
        else:
            self.wypelnienie = 0
        self.setWidthLoadingBar()
        logging.debug(f"changeLoadingBar metoda - Wypelnienie={self.wypelnienie}")

    def downloadPictures(self):
        logging.debug("downloadPictures")

    def setTimerDownloadPictures(self):
        logging.debug("setTimerDownloadPictures")
        self.timerDownloader = QtCore.QTimer()
        self.timerDownloader.timeout.connect(self.downloadPictures)
        timeToDownload=self.timeToDownloadPictures
        logging.debug(f"czasUruchomieniaPobrania: {timeToDownload} minself")
        self.timerDownloader.setInterval(timeToDownload)
        self.timerDownloader.start()

    def setTimerChangePicture(self):
        logging.debug("setTimerChangePicture")
        self.timerPicture = QtCore.QTimer()
        self.timerPicture.timeout.connect(self.changePicture)
        timeToChange=int(floor(int(self.czasObrazka)))
        logging.debug("czasObrazka:"+str(timeToChange) + "ms")
        self.timerPicture.setInterval(timeToChange)
        self.timerPicture.start()

    def setTimerLoadingBar(self):
        logging.debug("setTimerLoadingBar")
        self.timerLoadingBar = QtCore.QTimer()
        self.timerLoadingBar.timeout.connect(self.changeLoadingBar)
        timeToChange=int(floor(int(self.czasObrazka)/10))
        logging.debug("timeToChange:"+str(timeToChange))
        self.timerLoadingBar.setInterval(timeToChange)
        self.timerLoadingBar.start()

    def setSizeWindow(self):
        self.widthWindow = self.mainWindow.frameGeometry().width()
        self.heightWindow = self.mainWindow.frameGeometry().height()
        logging.debug("widthWindow :"+str(self.widthWindow))
        logging.debug("heightWindow :"+str(self.heightWindow))
        self.lab_MapOrWidget.setGeometry(QtCore.QRect(0, self.sizeOfLoadingBar, self.widthWindow, self.heightWindow))

class Window(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()
    def __init__(self, sizeOfLoadingBar, fullScreen, time, mapa, widget, kwadrat):
        super(Window, self).__init__(parent=None)
        self.ui = Ui_MainWindow(sizeOfLoadingBar, time)
        self.ui.setupUi(self)
        self.resized.connect(self.resizeEventFunction)
        if fullScreen:
            #self.showMaximized()
            self.showFullScreen()

    def resizeEvent(self, event):
        self.resized.emit()
        self.ui.setSizeWindow()
        return super(Window, self).resizeEvent(event)

    def resizeEventFunction(self):
        logging.debug("resizeEvent")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            logging.debug("Klawisz Escape został wciśniety")
            if self.isFullScreen():
                self.showMaximized()
                event.accept()
                logging.debug("wyłączony tryb pełnoekranowy")
        if event.key() == Qt.Key_Space :
            logging.debug("Klawisz Spacja został wciśniety")
            if self.isFullScreen()==False:
                self.showFullScreen()
                event.accept()
                logging.debug("włączono tryb pełnoekranowy")

if __name__ == "__main__":
    obecny_folder=os.getcwd()
    logging.debug(f"początkowy folder wykonywania:{obecny_folder}")
    args=def_params()
    #ustawioneParametry
    sizeOfLoadingBar=int(args.sizeOfLoadingBar)
    fullScreen=args.fullScreenSlideshow
    time=int(args.timeForPicture)
    workdirectory=args.workdirectory
    mapa=args.mapapng
    widget=args.widgetpng
    kwadrat=args.kwadratpng
    logging.debug(pprint(args))
    os.chdir(workdirectory)
    obecny_folder=os.getcwd()
    logging.debug(f"obecny folder roboczy:{obecny_folder}")
    #odpalenie aplikacji
    app = QtWidgets.QApplication(sys.argv)
    w = Window(sizeOfLoadingBar, fullScreen, time, mapa, widget, kwadrat)
    w.show()
    sys.exit(app.exec_())
