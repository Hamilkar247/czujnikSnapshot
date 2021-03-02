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
#from PIL import Image
from pprint import pprint
from pprint import pformat
from requests import Session
import requests
from urllib.request import urlopen

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
    parser.add_argument("-tp", "--timeForPicture", type=int, help="podaj czas w [s] dla każdego obrazka")
    parser.add_argument("-td", "--timeForDownloader", type=int, help="podaj czas w [s] jak często mają być pobierane pliki")
    parser.add_argument("-wd", "--workdirectory", help="argument wskazuje folder roboczy - wazny z tego wzgledu że tam powinien się znajdować plik konfiguracyjny")
    parser.add_argument("-pasek", "--pasekpng", help="url do ścieszki z png używanego w LoadingBar-ze - uwaga zalecany format png!")
    parser.add_argument("-sc", "--serwer_config", help="przechowuje url do serwera z plikiem jsonowy który będzie plikiem konfiguracyjnym")
    parser.add_argument("-d", "--discretizationLoadingBar", type=int, help="określa poziom dyskretyzacji")
    parser.add_argument("-p", "--port", type=int, help="numer portu na który będą wysyłane informacje o udanym pobraniu"),
    args = parser.parse_args()
    for key, value in list(args.__dict__.items()):
        if value is None or value == False:
            #print(f"usuniete {key} {value}")
            del args.__dict__[key]
    #print("after command line"))
    #pprint(args.__dict__))

    if os.path.exists('config.json'):
        config_args = argparse.Namespace()
        with open('config.json', 'rt') as f:
             config_args = argparse.Namespace()
             config_args.__dict__.update(json.load(f))
             #pprint(config_args)
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
        logging.debug(pformat(config_args.__dict__))
    return config_args

class Ui_MainWindow(object):

    def __init__(self, sizeOfLoadingBar, discretizationLoadingBar, timeForPicture, timeForDownloader, slajdy, workdirectory, serwer_config, port):
        logging.debug("UI_MainWindow __init__")
        self.lab_loadingbBar = None #label na loadingbara
        self.lab_slajd = None #label na widget/mape
        self.numerZdjecia = 0 #zmienna wskazuje nam numer obrazka który obecnie jest wyświetlany
        self.widthWindow = 925
        self.heightWindow = 810
        self.sizeOfLoadingBar = int(sizeOfLoadingBar)
        self.ustawienieCzasowTimerow(timeForDownloader, timeForPicture)
        self.sizeOfLoadingBar=int(sizeOfLoadingBar)
        self.discretizationLoadingBar=discretizationLoadingBar
        self.MainWindow = None
        self.slajdy = slajdy
        self.numerZdjecia=0
        self.pasekpng = pasek[0]
        self.wypelnienie = 0
        self.flag_UpdatePrzedChwilaConfiga=False
        self.liczbaPrzerwanychPolaczen=0
        self.workdirectory=workdirectory
        self.serwer_config=serwer_config
        self.segmentationTimeLoadingBar=1000 #czas w mikrosekundach jednego segmentu loadingBar
        self.port=port

        #timery
        self.timerDownloader = None
        self.timerFrame = None
        self.timerResetInnych = None

    def ustawienieCzasowTimerow(self, timeForDownloader, timeForPicture):
        self.czasObrazka = int(timeForPicture)*1000 #w milisekundach #bez int - napis zostanie ... wygenerowany 1000 razy
        self.timeForDownloader = int(timeForDownloader)*1000 #w milisekundach

    def setupUi(self, MainWindow):
        logging.debug("setupUi - inicjalne uruchomienie")
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
        self.lab_loadingBar.setPixmap(QtGui.QPixmap(self.pasekpng))
        self.lab_loadingBar.setScaledContents(True)
        #mapa i widget
        self.lab_slajd = QtWidgets.QLabel(MainWindow)
        self.lab_slajd.setGeometry(QtCore.QRect(0, self.sizeOfLoadingBar, self.widthWindow, self.heightWindow-self.sizeOfLoadingBar))
        self.lab_slajd.setText("")
        self.lab_slajd.setPixmap(QtGui.QPixmap(self.slajdy[self.numerZdjecia]['nazwapng']))
        self.lab_slajd.setScaledContents(True)
        self.lab_slajd.setObjectName("lab_slajd")
        #timery
        self.setTimerDownloadFiles()
        self.setTimerChangeFrame()
        #inicjalne pobranie
        logging.debug("inicjalne pobranie")
        self.downloadFiles()

    def setWidthLoadingBar(self):
        self.lab_loadingBar.setGeometry(QtCore.QRect(0,0, self.wypelnienie * (self.widthWindow/self.discretizationLoadingBar), self.sizeOfLoadingBar))

    def setLabelPicture(self):
        self.lab_slajd.setGeometry(QtCore.QRect(0, self.sizeOfLoadingBar, self.widthWindow, (self.heightWindow - self.sizeOfLoadingBar) ) )

    #uwaga - metoda verify dziala tylko dla png formatu
    def checkPicture(self, picturepng):
        brokenImage=False
        try:
            img = Image.open(picturepng)
            img.verify()
            logging.debug(f"Poprawny png {picturepng}")
            brokenImage=False
        except Exception:
            brokenImage=True
            logging.debug('Błąd przy odczycie zdjęcia {picturepng}')
        except FileExistsError:
            logging.debug(f"Nie znaleziono pliku: {picturepng}")
            brokenImage=True
        return brokenImage

    def changeFrame(self):
        logging.debug("metoda changeFrame")
        flagaZmianaZdjecia=False
        flagaZmianaZdjecia=self.changeLoadingBar()
        if flagaZmianaZdjecia == True:
            self.changePicture()
        self.setLabelPicture()
        self.setWidthLoadingBar()

    def changePicture(self):
        logging.debug(f"changePicture Function - numerZdjecia={self.numerZdjecia}")
        try:
            numer=self.numerZdjecia
            #brokenImage=self.checkPicture(self.slajdy[numer]['nazwapng'])
            #if brokenImage == False:

            pixmap = QtGui.QPixmap(self.slajdy[numer]['nazwapng'])
            self.lab_slajd.setPixmap(pixmap)
            #else:
            #    self.lab_slajd.setPixmap(QtGui.QPixmap(f"{self.slajdy[numer]}.bkp"))
            #    logging.debug(f"{self.slajdy[numer]})")
            if (len(self.slajdy)-1>numer):
                self.numerZdjecia = self.numerZdjecia+1
            else:
                self.numerZdjecia = 0
            self.wypelnienie = 0
        except IOError as error:
            print("Wystapil blad przy otwieraniu pliku {self.slajdy[numer]}")
        except Exception as error:
            print(f"wystapil blad przy przemianie zdjecia w changePicture {error}")
            numer=self.numerZdjecia=0

    def changeLoadingBar(self):
        flagaZmianaZdjecia=False
        if self.wypelnienie < self.discretizationLoadingBar:
            self.wypelnienie = self.wypelnienie+1
            flagaZmianaZdjecia=False
        else:
            self.wypelnienie = 0
            flagaZmianaZdjecia=True
        #logging.debug(f"changeLoadingBar metoda - Wypelnienie={self.wypelnienie}")
        return flagaZmianaZdjecia

    def checkLastModifiedTimePicture(self, slajd):
        czasUtworzenia=""
        flag_RozneDaty=False
        with urlopen(slajd['url']) as f:
            #logging.debug("Uwaga czasy są pokazywane w czasie uniwersalnym (greenwich)")
            czasUtworzenia=dict(f.getheaders())['Last-Modified']
            #logging.debug(f"slajd u nas: {slajd['dataUtworzenia']}")
            #logging.debug(f"slajd tam  : {czasUtworzenia}")
            #logging.debug(f"czy pobieramy? {flag_RozneDaty}")
            if czasUtworzenia==slajd['dataUtworzenia']:
                #logging.debug("data zdjecia nie zmieniła się")
                flag_RozneDaty=False
            else:
                slajd['dataUtworzenia']=czasUtworzenia
                flag_RozneDaty=True
        return flag_RozneDaty

    def checkLastModifiedTimeConfig(self, serwer_config):
        czasUtworzenia=""
        flag_RozneDaty=False
        with urlopen(serwer_config['url']) as f:
            #logging.debug("Uwaga czasy są pokazywane w czasie uniwersalnym (greenwich)")
            czasUtworzenia=dict(f.getheaders())['Last-Modified']
            #logging.debug(f"config u nas: {serwer_config['dataUtworzenia']}")
            #logging.debug(f"config tam  : {czasUtworzenia}")
            #logging.debug(f"czy pobieramy? {flag_RozneDaty}")
            if czasUtworzenia==serwer_config['dataUtworzenia']:
                #logging.debug("data configu nie zmieniła się")
                flag_RozneDaty=False
            else:
                logging.debug(f"nowa data configa na serwerze {czasUtworzenia}")
                serwer_config['dataUtworzenia']=czasUtworzenia
                flag_RozneDaty=True
        return flag_RozneDaty

    def downloadFiles(self):
        if self.flag_UpdatePrzedChwilaConfiga==False:
            logging.debug("----------------------------------------------")
            pprint(f" halo ! masz tu ! {self.slajdy}")
            logging.debug("downloadFiles")
            flagDownloadBroken=True
            flaga_czyCosPobrano=False
            try:
                logging.debug("downloadPictures")
                for slajd in list(self.slajdy):
                    flaga_pobierzZdjecie=False
                    flaga_pobierzZdjecie=self.checkLastModifiedTimePicture(slajd)
                    if flaga_pobierzZdjecie:
                        logging.debug(f"Przed pobraniem: slajd {slajd['nazwapng']} {slajd['dataUtworzenia']}")
                        r_slajd = requests.get(slajd['url'], allow_redirects=True)
                        with open(f"{slajd['nazwapng']}.download", 'wb') as file_slajd:
                            file_slajd.write(r_slajd.content)
                        #logging.debug(f"Data utworzenia pliku:{self.get_created_taken()}")
                        os.rename(f"{slajd['nazwapng']}.download", f"{slajd['nazwapng']}")
                        logging.debug(f"pobrano zdjęcia {slajd['nazwapng']} {slajd['dataUtworzenia']}")
                        flaga_czyCosPobrano=True
                print("zdjecia po sprawdzeniu")
                pprint(self.slajdy)

                logging.debug("downloadConfig")
                flaga_pobierzConfig=False
                if self.serwer_config['url'] == False:
                    print("ustawiona brak pobierania configa z serwera")
                else:
                    flaga_pobierzConfig=self.checkLastModifiedTimeConfig(self.serwer_config)
                    if flaga_pobierzConfig:
                        logging.debug(f"Przed pobraniem config {self.serwer_config['url']} {self.serwer_config['dataUtworzenia']}")
                        r_serwer_config = requests.get(serwer_config['url'], allow_redirects=True)
                        nazwa_zapisanego_configa='config.json'
                        with open(nazwa_zapisanego_configa, 'wb') as file_json:
                            file_json.write(r_serwer_config.content)
                        logging.debug(f"pobrano zapisany config o nazwie: {nazwa_zapisanego_configa}")
                        self.aktualizacjaConfigowychParametrow()

                        flaga_czyCosPobrano=True
                    if flaga_czyCosPobrano==True:
                        ###### WYSŁANIE SATUSU NA SERVER CZUJNIKI MIEJSKIE ZE WSZYSTKO JEST OK ########
                        session = Session()
                        # HEAD requests ask for *just* the headers, which is all you need to grab the
                        # session cookie
                        print("pobieranie w slideshow działa")
                        response = session.post(
                                    url='http://czujnikimiejskie.pl/apipost/add/measurement',
                                    data={"sn":str(self.port),"a":"1","w":"0","z":"0"},
                        )
                        print(response.text)
                flagDownloadBroken=False
            except requests.exceptions.RequestException as error:
                flagDownloadBroken=True
                print(f"Wystąpił problem z połączeniem:{error}")
            except Exception as error:
                flagDownloadBroken=True
                print(f"Wystąpił problem z połączeniem:{error}")
                print("Wykryto bład : "+str(error))
            if flagDownloadBroken==False:
                os.chdir('/tmp/')
                logging.debug(f"folder na plik tymczasowy: {os.getcwd()}")
                if os.path.isfile('working_slideshow.txt'):
                    logging.debug("working_slideshow.txt plik istnieje")
                else:
                    try:
                        f=open("working_slideshow.txt", "w+")
                    except FileNotFoundError:
                        logging.debug("Uszkodzony plik lub zła ścieszka")
                    logging.debug("stworzono working_slideshow.txt plik")
                os.chdir(self.workdirectory)
                logging.debug(f"Wracamy do folderu roboczego: {os.getcwd()}")
            logging.debug("koniec downloadFiles")

        else: #self.flag_UpdatePrzedChwilaConfiga==True:
            logging.debug("przed chwila zmieniono dane configa - pobieranie wstrzymane do kolejnej iteracji pobierania")
            self.flag_UpdatePrzedChwilaConfiga=False
        self.aktualnyStanZmiennychConfigowych()

    def updateZmiennych(self, config_args):
        logging.debug("updateZmiennych")
        self.ustawienieCzasowTimerow(config_args.timeForDownloader, config_args.timeForPicture)
        self.sizeOfLoadingBar=config_args.sizeOfLoadingBar
        self.slajdy=config_args.zdjeciaSlajd
        self.pasek=config_args.pasekpng[0]
        self.discretizationLoadingBar=discretizationLoadingBar
        self.port=config_args.port

    def aktualnyStanZmiennychConfigowych(self):
        print("---------stan-zmiennych-configowych---------")
        print(f"sizeOfLoadingBar      : {self.sizeOfLoadingBar}")
        print(f"pasek                 : {self.pasekpng}")
        print(f"czasObrazka           : {self.czasObrazka}")
        print(f"timeForDownloader     : {self.timeForDownloader}")
        print(f"discretizationLoadingBar:{self.discretizationLoadingBar}")
        print(f"port                  :{self.port}")
        print(f"slajdy          : {self.slajdy}")

    def aktualizacjaConfigowychParametrow(self):
        print("----*****************----")
        logging.debug("aktualizacjaConfigowychParametrow")
        if os.path.exists('config.json'):
            config_args = argparse.Namespace()
            #zczytuje configa bo sie zmienił
            with open('config.json', 'rt') as f:
                 config_args = argparse.Namespace()
                 config_args.__dict__.update(json.load(f))
                 #pprint(config_args)
            for key, value in list(config_args.__dict__.items()):
                if value == "False" or value == "false":
                    config_args.__dict__[key]=False
                elif value == "True" or value == "true":
                    config_args.__dict__[key]=True
                if key == "__comment__":
                    del config_args.__dict__[key]
            logging.debug("zczytane zmienne")
            pprint(config_args)

            #ustawiam zmienne z nowego configa, ktorych zmiana jest istotna
            self.updateZmiennych(config_args)

            # resetuje timery
            logging.debug("resetuje timery")
            self.stopTimerDownloadFiles()
            self.stopTimerChangeFrame()
            self.setTimerDownloadFiles()
            self.setTimerChangeFrame()
            self.flag_UpdatePrzedChwilaConfiga=True
        else:
            print("Brak pliku konfiguracyjnego - jeśli żadnego nie posiadasz prośba o skopiowanie \n     config.json.example i nazwanie owej kopii config.json")

    def setTimerChangeFrame(self):
        logging.debug("setTimerChangeFrame")
        self.timerFrame = QtCore.QTimer()
        self.timerFrame.timeout.connect(self.changeFrame)
        timeToChangePicture=int(floor(int(self.czasObrazka)))
        logging.debug(f"czasObrazka:{str(timeToChangePicture)} ms")
        self.segmentationTimeLoadingBar=int(floor(int(self.czasObrazka)/self.discretizationLoadingBar))
        self.timerFrame.setInterval(self.segmentationTimeLoadingBar)
        logging.debug(f"timeToChange:{str(self.segmentationTimeLoadingBar)} ms")
        self.timerFrame.start()

    def stopTimerChangeFrame(self):
        self.timerFrame.stop()
        print(f"ahoj stopuje timerFrame")

    def setTimerDownloadFiles(self):
        logging.debug("setTimerDownloadFiles")
        self.timerDownloader = QtCore.QTimer()
        self.timerDownloader.timeout.connect(self.downloadFiles)
        timeForDownloader=self.timeForDownloader
        logging.debug(f"czasUruchomieniaPobrania: {timeForDownloader} minisekund")
        self.timerDownloader.setInterval(timeForDownloader)
        self.timerDownloader.start()

    def setSizeWindow(self):
        self.widthWindow = self.mainWindow.frameGeometry().width()
        self.heightWindow = self.mainWindow.frameGeometry().height()
        logging.debug("widthWindow :"+str(self.widthWindow))
        logging.debug("heightWindow :"+str(self.heightWindow))
        self.setLabelPicture()
        self.setWidthLoadingBar()

class Window(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()
    def __init__(self, sizeOfLoadingBar, discretizationLoadingBar, fullScreen, timeForPicture, timeForDownloader, pasek, slajdy, workdirectory, serwer_config, port):
        super(Window, self).__init__(parent=None)
        self.ui = Ui_MainWindow(sizeOfLoadingBar, discretizationLoadingBar, timeForPicture, timeForDownloader, slajdy, workdirectory, serwer_config, port)
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
    timeForPicture=int(args.timeForPicture)
    timeForDownloader=int(args.timeForDownloader)
    discretizationLoadingBar=int(args.discretizationLoadingBar)
    workdirectory=args.workdirectory
    pasek=args.pasekpng
    slajdy=args.zdjeciaSlajd
    port=args.port
    pprint(slajdy)
    serwer_config = { "url": args.serwer_config, "dataUtworzenia": "" }
    logging.debug(pformat(args))
    os.chdir(workdirectory)
    obecny_folder=os.getcwd()
    logging.debug(f"obecny folder roboczy:{obecny_folder}")
    #odpalenie aplikacji
    app = QtWidgets.QApplication(sys.argv)
    w = Window(sizeOfLoadingBar, discretizationLoadingBar, fullScreen, timeForPicture, timeForDownloader, pasek, slajdy, workdirectory, serwer_config, port)
    w.show()
    sys.exit(app.exec_())
