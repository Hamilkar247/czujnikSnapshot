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
            parametry do wyswietlenia
            """
            )
    parser.add_argument("-l", "--log", action='store_true', help="ustaw debug flage")
    parser.add_argument("-g", "--grubosc", default=4, help="ustaw grubosc gifa")
    parser.add_argument("-f", "--fullScreen", action='store_true', help="ustaw maksymalny rozmiar")
    parser.add_argument("-t", "--timeSeq", default=9960, help="podaj czas w [ms] dla każdego obrazka - pamietaj że przepływ gifa jest niezależny od tego")
    args = parser.parse_args()
    if args.log:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Ten komunikat pokazuje sie tylko w trybie debug")
        print("args:" + str(args))
    return args

class Ui_MainWindow(object):

    def __init__(self, gruboscGifa, timeSeq):
        logging.debug("UI_MainWindow __init__")
        self.label = None #label na gifa
        self.label_2 = None #label na widget/mape
        self.movie = None #movie do odpalenia gifa
        self.timer = None #timer do zamiany zdjęć
        self.flagaWidget = 1 #flaga mowiaca czy jest teraz mapa czy widget
        self.centralWidget = None
        self.widthWindow = 925
        self.heightWindow = 810
        self.gruboscGifa = int(gruboscGifa)
        self.timeSeq = timeSeq
        self.MainWindow = None
        self.timer = None
        self.mapapng = None
        self.widgetpng = None
        self.gif = None
        self.kwadratpng = None
        self.timerLoadingBar = None
        self.wypelnienie = 1
        
        self.readURLPictures()

    #wczytywanie nazw grafik z pliku slideshow.json
    def readURLPictures(self):
        logging.debug("readURLPictures")
        with open('slideshow.json') as json_file:
            urls = json.load(json_file)
            self.mapapng=urls['mapa']
            self.widgetpng=urls['widget']
            self.gif=urls['gif']
            self.kwadratpng=urls['kwadrat']

    def setupUi(self, MainWindow):
        logging.debug("setupUi")
        self.mainWindow = MainWindow
        self.mainWindow.setObjectName("MainWindow")
        self.mainWindow.setWindowTitle("MainWindow")
        self.mainWindow.resize(self.widthWindow, self.heightWindow)
        #self.lab_gif = QtWidgets.QLabel(self.mainWindow)
        #self.lab_gif.setGeometry(QtCore.QRect(0, 0, self.widthWindow, self.gruboscGifa))
        #self.lab_gif.setText("")
        #self.lab_gif.setScaledContents(True)
        #self.lab_gif.setObjectName("lab_gif")
        #self.movie = QMovie(self.gif)
        #self.lab_gif.setMovie(self.movie)
        #self.movie.start()
       #pasek u góry
        self.lab_Pasek = QtWidgets.QLabel(self.mainWindow)
        self.setWidthLoadingBar()
        self.lab_Pasek.setText("")
        self.lab_Pasek.setScaledContents(True)
        self.lab_Pasek.setObjectName("lab_Pasek")
        self.lab_Pasek.setPixmap(QtGui.QPixmap(self.kwadratpng))
        self.lab_Pasek.setScaledContents(True)
        self.lab_MapOrWidget = QtWidgets.QLabel(MainWindow)
        self.lab_MapOrWidget.setGeometry(QtCore.QRect(0, self.gruboscGifa, self.widthWindow, self.heightWindow-20))
        self.lab_MapOrWidget.setText("")
        self.lab_MapOrWidget.setPixmap(QtGui.QPixmap(self.mapapng))
        self.lab_MapOrWidget.setScaledContents(True)
        self.lab_MapOrWidget.setObjectName("lab_MapOrWidget")
        self.setTimerChangePicture()
        self.setTimerLoadingBar()

    def setWidthLoadingBar(self):
        self.lab_Pasek.setGeometry(QtCore.QRect(0,0, self.wypelnienie * self.widthWindow/10, self.gruboscGifa))

    def changePicture(self):
        logging.debug("changePicture Function - flagWidget="+str(self.flagaWidget))
        if self.flagaWidget == 0:
            self.lab_MapOrWidget.setPixmap(QtGui.QPixmap(self.mapapng))
            self.flagaWidget = 1
        else:
            self.restartGifa
            self.lab_MapOrWidget.setPixmap(QtGui.QPixmap(self.widgetpng))
            self.flagaWidget = 0
            self.restartGifa()

    def changeLoadingBar(self):
        if self.wypelnienie < 10:
            self.wypelnienie = self.wypelnienie+1
        else:
            self.wypelnienie = 1
        self.setWidthLoadingBar()
        logging.debug(f"changeLoadingBar metoda - Wypelnienie={self.wypelnienie}")

    def setTimerChangePicture(self):
        logging.debug("setTimerChangePicture")
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.changePicture)
        timeToChange=int(floor(int(self.timeSeq)))
        logging.debug("timeSeq:"+str(timeToChange))
        self.timer.setInterval(timeToChange)
        self.timer.start()

    def setTimerLoadingBar(self):
        logging.debug("setTimerLoadingBar")
        #self.timerLoadingBar.timeout.connect(floor(int(self.timeSeq)/10))
        self.timer.timeout.connect(self.changeLoadingBar)

    def restartGifa(self):
        logging.debug("restartGifa")
        #self.movie.stop()
        #self.lab_gif.setMovie(self.movie)
        #self.movie.start()

    def setSizeWindow(self):
        self.widthWindow = self.mainWindow.frameGeometry().width()
        self.heightWindow = self.mainWindow.frameGeometry().height()
        logging.debug("widthWindow :"+str(self.widthWindow))
        logging.debug("heightWindow :"+str(self.heightWindow))
        self.lab_MapOrWidget.setGeometry(QtCore.QRect(0, self.gruboscGifa, self.widthWindow, self.heightWindow))
        #self.lab_gif.setGeometry(QtCore.QRect(0, 0, self.widthWindow, self.gruboscGifa))

class Window(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()
    def __init__(self, gruboscGifa, fullScreen, timeSeq):
        super(Window, self).__init__(parent=None)
        self.ui = Ui_MainWindow(gruboscGifa, timeSeq)
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
    gruboscGifa=args.grubosc
    fullScreen=args.fullScreen
    timeSeq=args.timeSeq
    app = QtWidgets.QApplication(sys.argv)
    w = Window(gruboscGifa, fullScreen, timeSeq)
    w.show()
    sys.exit(app.exec_())
