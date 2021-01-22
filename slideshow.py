# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie
from PyQt5.Qt import Qt
import time
import sys
import logging
import argparse
import json
from math import floor

def def_params():
    parser = argparse.ArgumentParser(
            description=
            """
            Klawisze akcji:
            - spacja - przejście w tryb pełnoekranowy
            - escape - wyjście z trybu pełnoekranowego
            parametry do wyswietlenia:
            """
            )
    parser.add_argument("-l", "--log", action='store_true', help="ustaw flage 'debug' i wyswietlaj logi")
    parser.add_argument("-g", "--grubosc", default=4, help="ustaw grubosc loadingBara")
    parser.add_argument("-f", "--fullScreen", action='store_true', help="ustaw maksymalny rozmiar")
    parser.add_argument("-t", "--time", default=10, help="podaj czas w [s] dla każdego obrazka")
    args = parser.parse_args()
    if args.log:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Ten komunikat pokazuje sie tylko w trybie debug")
        print("args:" + str(args))
    return args

class Ui_MainWindow(object):

    def __init__(self, gruboscLoadingBara, time):
        logging.debug("UI_MainWindow __init__")
        self.lab_loadingbBar = None #label na loadingbara
        self.lab_MapOrWidget = None #label na widget/mape
        self.movie = None #movie do odpalenia gifa
        self.timerPicture = None #timerPicture do zamiany zdjęć
        self.flagaWidget = 1 #flaga mowiaca czy jest teraz mapa czy widget
        self.centralWidget = None
        self.widthWindow = 925
        self.heightWindow = 810
        self.gruboscLoadingBara = int(gruboscLoadingBara)
        self.czasObrazka = int(time)*1000 #w milisekundach #bez int - napis zostanie ... wygenerowany 1000 razy
        self.MainWindow = None
        self.mapapng = None
        self.widgetpng = None
        self.kwadratpng = None
        self.timerLoadingBar = None
        self.wypelnienie = 0
        self.readURLPictures()
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

    #wczytywanie nazw grafik z pliku slideshow.json
    def readURLPictures(self):
        logging.debug("readURLPictures")
        with open('slideshowConfig.json') as json_file:
            urls = json.load(json_file)
            self.mapapng=urls['mapa']
            self.widgetpng=urls['widget']
            self.kwadratpng=urls['kwadrat']

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
        self.lab_MapOrWidget.setGeometry(QtCore.QRect(0, self.gruboscLoadingBara, self.widthWindow, self.heightWindow-20))
        self.lab_MapOrWidget.setText("")
        self.lab_MapOrWidget.setPixmap(QtGui.QPixmap(self.mapapng))
        self.lab_MapOrWidget.setScaledContents(True)
        self.lab_MapOrWidget.setObjectName("lab_MapOrWidget")
        #timery
        self.setTimerChangePicture()
        self.setTimerLoadingBar()

    def setWidthLoadingBar(self):
        self.lab_loadingBar.setGeometry(QtCore.QRect(0,0, self.wypelnienie * self.widthWindow/10, self.gruboscLoadingBara))

    def changePicture(self):
        logging.debug("changePicture Function - flagWidget="+str(self.flagaWidget))
        if self.flagaWidget == 0:
            self.lab_MapOrWidget.setPixmap(QtGui.QPixmap(self.mapapng))
            self.flagaWidget = 1
            self.wypelnienie = 0
            self.setWidthLoadingBar()
        else:
            self.lab_MapOrWidget.setPixmap(QtGui.QPixmap(self.widgetpng))
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
        self.lab_MapOrWidget.setGeometry(QtCore.QRect(0, self.gruboscLoadingBara, self.widthWindow, self.heightWindow))

class Window(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()
    def __init__(self, gruboscLoadingBara, fullScreen, time):
        super(Window, self).__init__(parent=None)
        self.ui = Ui_MainWindow(gruboscLoadingBara, time)
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
    args=def_params()
    gruboscLoadingBara=args.grubosc
    fullScreen=args.fullScreen
    time=args.time
    logging.debug(f"args : {args}")
    app = QtWidgets.QApplication(sys.argv)
    w = Window(gruboscLoadingBara, fullScreen, time)
    w.show()
    sys.exit(app.exec_())
