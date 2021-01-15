# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie
import time
import sys
import logging
import argparse
import json
from math import floor

def def_params():
    parser = argparse.ArgumentParser(
            description="parametry do wyswietlenia"
    )
    parser.add_argument("-l", "--log", action='store_true', help="ustaw debug flage")
    parser.add_argument("-g", "--grubosc", default=20, help="ustaw grubosc gifa")
    parser.add_argument("-f", "--fullScreen", action='store_true', help="ustaw maksymalny rozmiar")
    parser.add_argument("-t", "--timeSeq", default=9960, help="podaj czas w [ms] całej sekwencji - pamietaj że przepływ gifa jest niezależny od tego")
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

        self.readURLPictures()

    #wczytywanie nazw grafik z pliku slideshow.json
    def readURLPictures(self):
        with open('slideshow.json') as json_file:
            urls = json.load(json_file)
            print(urls)
            print(urls['mapa'])

    def setupUi(self, MainWindow):
        logging.debug("setupUi")
        self.mainWindow = MainWindow
        self.mainWindow.setObjectName("MainWindow")
        self.mainWindow.setWindowTitle("MainWindow")
        self.mainWindow.resize(self.widthWindow, self.heightWindow)
        self.lab_gif = QtWidgets.QLabel(self.mainWindow)
        self.lab_gif.setGeometry(QtCore.QRect(0, 0, self.widthWindow, self.gruboscGifa))
        self.lab_gif.setText("")
        self.lab_gif.setScaledContents(True)
        self.lab_gif.setObjectName("lab_gif")
        self.movie = QMovie("10s.gif")
        self.lab_gif.setMovie(self.movie)
        self.movie.start()
        self.lab_MapOrWidget = QtWidgets.QLabel(MainWindow)
        self.lab_MapOrWidget.setGeometry(QtCore.QRect(0, self.gruboscGifa, self.widthWindow, self.heightWindow-20))
        self.lab_MapOrWidget.setText("")
        self.lab_MapOrWidget.setPixmap(QtGui.QPixmap("kolno_map.png"))
        self.lab_MapOrWidget.setScaledContents(True)
        self.lab_MapOrWidget.setObjectName("lab_MapOrWidget")
        self.setTimerChangePicture()

    def changePicture(self):
        logging.debug("changePicture Function - flagWidget="+str(self.flagaWidget))
        if self.flagaWidget == 0:
            self.lab_MapOrWidget.setPixmap(QtGui.QPixmap("kolno_map.png"))
            self.flagaWidget = 1
        else:
            self.restartGifa
            self.lab_MapOrWidget.setPixmap(QtGui.QPixmap("widget_kolno.png"))
            self.flagaWidget = 0
            self.restartGifa()

    def setTimerChangePicture(self):
        logging.debug("setTimerChangePicture")
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.changePicture)
        timeToChange=int(floor(int(self.timeSeq)/2))
        logging.debug("timeSeq/2:"+str(timeToChange))
        self.timer.setInterval(timeToChange)
        self.timer.start()

    def restartGifa(self):
        logging.debug("restartGifa")
        self.movie.stop()
        self.lab_gif.setMovie(self.movie)
        self.movie.start()

    def setSizeWindow(self):
        self.widthWindow = self.mainWindow.frameGeometry().width()
        self.heightWindow = self.mainWindow.frameGeometry().height()
        logging.debug("widthWindow :"+str(self.widthWindow))
        logging.debug("heightWindow :"+str(self.heightWindow))
        self.lab_MapOrWidget.setGeometry(QtCore.QRect(0, self.gruboscGifa, self.widthWindow, self.heightWindow))
        self.lab_gif.setGeometry(QtCore.QRect(0, 0, self.widthWindow, self.gruboscGifa))

class Window(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()
    def __init__(self, gruboscGifa, fullScreen, timeSeq):
        super(Window, self).__init__(parent=None)
        self.ui = Ui_MainWindow(gruboscGifa, timeSeq)
        self.ui.setupUi(self)
        self.resized.connect(self.resizeEventFunction)
        if fullScreen:
            self.showMaximized()

    def resizeEvent(self, event):
        self.resized.emit()
        self.ui.setSizeWindow()
        return super(Window, self).resizeEvent(event)

    def resizeEventFunction(self):
        logging.debug("resizeEvent")

if __name__ == "__main__":
    args=def_params()
    gruboscGifa=args.grubosc
    fullScreen=args.fullScreen
    timeSeq=args.timeSeq
    app = QtWidgets.QApplication(sys.argv)
    w = Window(gruboscGifa, fullScreen, timeSeq)
    w.show()
    sys.exit(app.exec_())
