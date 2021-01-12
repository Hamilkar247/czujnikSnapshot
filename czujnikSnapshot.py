#!/bin/python3
import logging
import argparse
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options
import os
import json
from time import sleep
import datetime
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QTimer

class CzujnikSnap():
   #loghami=False

   def readConfigFunction(self):
       with open('config.json') as f:
           data = json.load(f)
       if self.loghami:
           logging.debug("readConfig")
           logging.debug(data)

   def seleniumWork(self):
       self.options = webdriver.ChromeOptions()
       if self.loghami:
           self.options.headless=False
       else:
           self.options.headless=True
       driver = webdriver.Chrome(options=self.options)
       url='http://czujnikimiejskie.pl/public/kozienice/'
       driver.get(url)
       sleep(5)
       screenshot = driver.save_screenshot('mapa.png')
       driver.close()

   def start(self):
       print("czujnikSnap")
       self.readConfigFunction()
       self.seleniumWork()

   def __init__(self, args):
      self.loghami = args.loghami

class App(QWidget):

    def __init__(self, url_map, url_widget):
        super().__init__()
        self.title = "CzujnikImage"
        self.left = 10
        self.top = 10
        self.width = 10
        self.height = 400
        self.url_map = url_map
        self.url_widget = url_widget
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        #Create widget
        label = QLabel(self)
        pixmap = QPixmap(self.url_map)
        label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        QTime
        label = QLabel(self)
        pixmap = QPixmap(self.url_widget)
        label.setPixmap(pixmap)

        self.show()

def def_params():
    parser = argparse.ArgumentParser(
            description="Description to fill"
    )
    parser.add_argument("-l", "--loghami", action='store_true', help="set debug")
    args = parser.parse_args()
    if args.loghami:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Only shown in debug mode")
        print("args:" + str(args))
    return args

def addCurrentFolderToPath():
    path_to_dir = os.path.dirname(os.path.realpath(__file__))
    os.environ["PATH"] += os.pathsep + path_to_dir

def main():
    args=def_params()
    addCurrentFolderToPath()
    #czuj = CzujnikSnap(args)
    #czuj.start()
    app = QApplication(sys.argv)
    ex = App('kolno_map.png', 'widget_kolno.png')
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
