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

def def_params():
    parser = argparse.ArgumentParser(
            description=
            """
CzujnikSnapshot - odpowiada za snapy z pomiarów danego urządzenia podanego
czujnika
            """
    )
    parser.add_argument("-l", "--loghami", action='store_true', help="ustaw tryb debug")
    parser.add_argument("-t", "--time", default=10, help="flaga określająca jak często ma być dokonywany snap czujnika")
    args = parser.parse_args()
    if args.loghami:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Komunikat pokazywany wyłącznie w trybie debug")
        print("args:" + str(args))
    return args

def addCurrentFolderToPath():
    path_to_dir = os.path.dirname(os.path.realpath(__file__))
    os.environ["PATH"] += os.pathsep + path_to_dir

class CzujnikSnap():
   def __init__(self, loghami, time_to_snap):
      self.loghami = loghami
      self.time_to_snap = time_to_snap
      self.mapa = None
      self.widget = None

   def readConfigFunction(self):
       logging.debug("readConfig")
       with open('config.json') as json_file:
           urls = json.load(json_file)
           self.mapa = urls['mapa']
           self.widget=urls['widget']
       logging.debug("mapa :"+self.mapa)
       logging.debug("widget:"+self.widget)

   def start(self):
       print("czujnikSnap")
       self.seleniumWork()

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

def main():
    args=def_params()
    loghami=args.loghami
    time=args.time
    addCurrentFolderToPath()
    czuj = CzujnikSnap(loghami, time)
    czuj.start()

if __name__ == "__main__":
    main()
