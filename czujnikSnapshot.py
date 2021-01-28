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
import subprocess
from PIL import Image

def def_params():
    parser = argparse.ArgumentParser(
            description=
            """
CzujnikSnapshot - odpowiada za snapy z pomiarów danego urządzenia podanego
czujnika

UWAGA - plik konfiguracyjny przyjmuje dla parametrów nastepujące stringi jako wartości logiczne 
True true - boolean True w pythonie
False false - boolean false w pythonie

            """
    )
    parser.add_argument("-l", "--loghami", action='store_true', help="ustaw tryb debug")
    parser.add_argument("-v", "--visible", action='store_true', help="odpalenie progromu bez trybu headless")
    parser.add_argument("-t", "--time", help="flaga określająca jak często ma być dokonywany snap czujnika")
    parser.add_argument("-wd", "--workdirectory", default="/home/matball/Projects/czujnikSnapshot", help="argument określa folder roboczy projektu - o tyle istotne, że w owym folderze szuka plików konfiguracyjnych json")
    parser.add_argument("-ch", "--chromiumurl", default="/usr/bin/chromium-browser", help="zmienna przechowująca link do chromium-browser")

    args = parser.parse_args()
    for key, value in args.__dict__.items():
        if value == None or value == False:
            del args.__dict__[key]
            break

    if os.path.exists('config.json'):
        config_args = argparse.Namespace()
        with open('config.json', 'rt') as f:
             config_args = argparse.Namespace()
             config_args.__dict__.update(json.load(f))
             print(config_args)
             print("dodaniu")
             config_args.__dict__.update(vars(args))
        for key, value in config_args.__dict__.items():
            if value == "False" or value == "false":
                print(f"{key} {value}")
                config_args.__dict__[key]=False
            elif value == "True" or value == "true":
                print(f"{key} {value}")
                config_args.__dict__[key]=True
    else:
        print("Brak pliku konfiguracyjnego - jeśli żadnego nie posiadasz prośba o skopiowanie \n config.json.example i nazwanie owej kopii config.json")

    if config_args.loghami:
        logging.basicConfig(level=logging.DEBUG, force=True)
        logging.debug("Komunikat pokazywany wyłącznie w trybie debug")
        print(f"config_args: {config_args}")

    return config_args

def addCurrentFolderToPath():
    path_to_dir = os.path.dirname(os.path.realpath(__file__))
    os.environ["PATH"] += os.pathsep + path_to_dir

class CzujnikSnap():
   def __init__(self, loghami, visible, time_to_snap, chromiumurl):
      self.loghami = loghami
      self.visible = visible
      self.time_to_snap = time_to_snap
      self.chromiumurl = chromiumurl
      self.mapa = None
      self.widget = None
      self.options = None
      self.driver = None
      self.start()

   def readConfigFunction(self):
       logging.debug("readConfigFunction")
       with open('config.json') as json_file:
           urls = json.load(json_file)
           self.mapa = urls['mapa-link']
           self.widget=urls['widget-link']
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
       self.options.binary_location = self.chromiumurl
       logging.debug(f"chromiumurl:{self.chromiumurl}")
       if self.visible:
           self.options.headless=False
       else:
           self.options.headless=True
       logging.debug(f"headless mode is: {self.options.headless}")
       logging.debug(f"options: {self.options}")
       #driver przeglądarki
       self.driver = webdriver.Chrome(options=self.options)
       self.driver.set_window_size(1920,1316)
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

   #Uwaga img.verify działa tylko dla png formatu
   def backupScreen(self, nameOfPicture):
       if os.path.exists(nameOfPicture):
           img = Image.open(f'{nameOfPicture}')
           logging.debug(f'{nameOfPicture}')
           brokenImage=False
           try:
               img.verify()
               print('Valid image')
               brokenImage=False
           except FileExistError:
               print(f'nie znaleziono pliku {nameOfPicture}.png')
           except Exception:
               print('Invalid image')
               logging.debug("Zdjęcia jest błędne, backup nie został nadpisany")
               brokenImage=True
           if brokenImage==False:
               copyFile = subprocess.Popen(['cp', f'{nameOfPicture}', f'{nameOfPicture}.bkp'], stdout=subprocess.PIPE)
               execute = copyFile.stdout.read()
               logging.debug(f'zrobiono kopie {nameOfPicture}.bkp')
       else:
           print(f"nie znaleziono zdjęcia {nameOfPicture}")


   def snapWidget(self):
       logging.debug("snapWidget - robienie zdjęcia widgetu")
       milli_sec = int(round(time.time()*1000))
       now = datetime.now()
       t = now.strftime("[%Y/%m/%d-%H:%M:%S]")
       logging.debug(f"driver: {self.driver}")
       self.driver.get(self.widget+str(milli_sec))
       self.backupScreen('widget.png')
       sleep(3)
       screenshot = self.driver.save_screenshot('widget.png')
       print(t, " ScreenShoot: Widget ")

   def snapMapa(self):
       logging.debug("snapMapa - robienie zdjęcia mapy")
       milli_sec = int(round(time.time()*1000))
       now = datetime.now()
       t = now.strftime("[%Y/%m/%d-%H:%M:%S]")
       self.driver.get(self.mapa+str(milli_sec))
       self.backupScreen('mapa.png')
       sleep(3)
       screenshot = self.driver.save_screenshot('mapa.png')
       print(t, " ScreenShoot: Mapa ")

def main():
    obecny_folder=os.getcwd()
    logging.debug(f"początkowy folder wykonywania:{obecny_folder}")
    args=def_params()
    loghami=args.loghami
    visible=args.visible
    workdirectory=args.workdirectory
    chromiumurl=args.chromiumurl
    os.chdir(workdirectory)
    obecny_folder=os.getcwd()
    logging.debug(f"obecny folder roboczy:{obecny_folder}")
    time=args.time
    display = Display(visible=0, size=(1920,1200))
    addCurrentFolderToPath()
    czuj = CzujnikSnap(loghami, visible, time, chromiumurl)
    display = display.stop()

if __name__ == "__main__":
    main()
