#!/bin/python3
import logging
import argparse
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options
import os
import json
from time import sleep
from datetime import datetime
import sys
import time

def def_params():
    parser = argparse.ArgumentParser(
            description=
            """
CzujnikSnapshot - odpowiada za snapy z pomiarów danego urządzenia podanego
czujnika
            """
    )
    parser.add_argument("-l", "--loghami", action='store_true', help="ustaw tryb debug")
    parser.add_argument("-v", "--visible", action='store_true', help="odpalenie progromu bez trybu headless")
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
      self.options = None
      self.driver = None
      self.start()

   def readConfigFunction(self):
       logging.debug("readConfigFunction")
       with open('czujnikSnapConfig.json') as json_file:
           urls = json.load(json_file)
           self.mapa = urls['mapa']
           self.widget=urls['widget']
       logging.debug("mapa :"+self.mapa)
       logging.debug("widget:"+self.widget)

   def start(self):
       logging.debug("start: czujnikSnap")
       self.readConfigFunction()
       #opcje przeglądarki
       self.options = Options()
       self.options.add_argument("--no-sandbox")
       self.options.add_argument("--start-fullscreen")
       self.options.add_argument("--kiosk")
       self.options.add_argument("--disable-application-cache")
       if self.loghami:
           self.options.headless=False
       else:
           self.options.headless=True
       logging.debug(f"headless mode is: {self.options.headless}")
       logging.debug(f"options: {self.options}")
       #driver przeglądarki
       self.driver = webdriver.Chrome(options=self.options)
       #self.driver.set_window_size(1920,1316)
       self.driver.set_script_timeout(30)
       self.driver.set_page_load_timeout(30) # seconds
       logging.debug(f"driver: {self.driver}")
       self.seleniumJob()

   def seleniumJob(self):
       logging.debug("seleniumJob - method")
       while True:
           self.snapWidget()
           self.snapMapa()
       self.driver.quit()

   def snapWidget(self):
       logging.debug("snapWidget - robienie zdjęcia widgetu")
       milli_sec = int(round(time.time()*1000))
       now = datetime.now()
       t = now.strftime("[%Y/%m/%d-%H:%M:%S]")
       logging.debug(f"driver: {self.driver}")
       self.driver.get(self.widget+str(milli_sec))
       sleep(3)
       screenshot = self.driver.save_screenshot('widget.png')
       print(t, " ScreenShoot: Widget ")

   def snapMapa(self):
       logging.debug("snapMapa - robienie zdjęcia widgetu")
       milli_sec = int(round(time.time()*1000))
       now = datetime.now()
       t = now.strftime("[%Y/%m/%d-%H:%M:%S]")
       self.driver.get(self.mapa+str(milli_sec))
       sleep(3)
       screenshot = self.driver.save_screenshot('mapa.png')
       print(t, " ScreenShoot: Mapa ")

def main():
    args=def_params()
    loghami=args.loghami
    time=args.time
    display = Display(visible=0, size=(1920,1200))
    addCurrentFolderToPath()
    czuj = CzujnikSnap(loghami, time)
    display = display.stop()

if __name__ == "__main__":
    main()
