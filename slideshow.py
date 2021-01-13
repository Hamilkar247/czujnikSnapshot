# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'szablon.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie
import time
import sys

class Ui_MainWindow(object):#WizardPage(object):

    def __init__(self):
        self.label = None #label na gifa
        self.label_2 = None #label na widget/mape
        self.movie = None #movie do odpalenia gifa
        self.timer = None #timer do zamiany zdjęć
        self.flagaWidget = 1 #flaga mowiaca czy jest teraz mapa czy widget
        self.centralWidget = None
        self.widthWindow = 925
        self.heightWindow = 810

    def setupUi(self, MainWindow):#WizardPage):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("MainWindow")
        MainWindow.resize(self.widthWindow, self.heightWindow)
        #self.label = QtWidgets.QLabel(WizardPage)
        #self.label.setGeometry(QtCore.QRect(0, 0, 931, 21))
        #self.label.setText("")
        #self.label.setScaledContents(True)
        #self.label.setObjectName("label")
        #self.movie = QMovie("10s.gif")
        #self.label.setMovie(self.movie)
        #self.movie.start()
        ########self.centralwidget = QtWidgets.QWidget(MainWindow)
        ########self.centralWidget.setObjectName("centralwidget")
        ########MainWindow.setCentralWidget(self.centralWidget)
        #MainWindow.resized.connect(self.someFunction)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.label_2 = QtWidgets.QLabel(MainWindow)#WizardPage)
        self.label_2.setGeometry(QtCore.QRect(0, 20, self.widthWindow, self.heightWindow))
        self.label_2.setText("matko boska")
        self.label_2.setPixmap(QtGui.QPixmap("kolno_map.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #self.timer = QtCore.QTimer()
        #self.timer.timeout.connect(self.changePicture)
        #self.timer.setInterval(4980)
        #self.timer.start()

    def changePicture(self):
        if self.flagaWidget == 0:
            self.label_2.setPixmap(QtGui.QPixmap("kolno_map.png"))
            self.flagaWidget = 1
        else:
            self.label_2.setPixmap(QtGui.QPixmap("widget_kolno.png"))
            self.flagaWidget = 0
            self.restartGifa

    def restartGifa(self):
        self.movie.stop()
        self.label.setMovie(self.movie)
        self.movie.start()

class Window(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(Window, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.resized.connect(self.someFunction)

    def resizeEvent(self, event):
        self.resized.emit()
        self.ui.changePicture()
        return super(Window, self).resizeEvent(event)

    def someFunction(self):
        print("someFunction")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    #WizardPage = QtWidgets.QWizardPage()
    w = Window()
    w.show()
   # MainWindow = QtWidgets.QMainWindow()
   # ui = Ui_WizardPage()

   # ui.setupUi(MainWindow)#WizardPage)
   # MainWindow.show()#WizardPage.show()
    sys.exit(app.exec_())
