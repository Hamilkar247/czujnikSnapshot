# -*- coding: utf-8 -*-
from json import JSONDecodeError

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import Qt
import sys
import os
import logging
import argparse
import json
from math import floor
# from PIL import Image
from pprint import pprint
from pprint import pformat
from requests import Session
import requests
from urllib.request import urlopen
import traceback

from gsm_slideshow.gsm_slideshow import GsmSlideshow


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
    # UWAGA - nie dopisuj argumentom wartości default - do takich wartości używamy tylko i wyłącznie plik konfiguracyjny
    parser.add_argument("-l", "--debug_logslideshow", action='store_true', help="ustaw flage 'debug' i wyswietlaj logi")
    parser.add_argument("-lu", "--debug_logusim800", action='store_true', help="wyświetlaj logi z usim800 (pobieranie GSM)")
    parser.add_argument("-md", "--mode_download", help="tryb pobierania - do wyboru jeden z trzech : both, wifi, gsm" )
    parser.add_argument("-path", "--path_gsm", help="ścieszka do urządzenia gsm")
    parser.add_argument("-b", "--baudrate", type=int, help="baudrate do przesyłania danych")
    parser.add_argument("-s", "--sizeOfLoadingBar", help="ustaw rozmiar(grubość) loadingBara")
    parser.add_argument("-f", "--fullScreenSlideshow", action='store_true',
                        help="ustaw maksymalny rozmiar programu przy odpaleniu programu")
    parser.add_argument("-tp", "--timeForPicture", type=int, help="podaj czas w [s] dla każdego obrazka")
    parser.add_argument("-td", "--timeForDownloader", type=int,
                        help="podaj czas w [s] jak często mają być pobierane pliki")
    parser.add_argument("-wd", "--workdirectory",
                        help="argument wskazuje folder roboczy - wazny z tego wzgledu że tam powinien się znajdować plik konfiguracyjny")
    parser.add_argument("-pasek", "--pasekpng",
                        help="url do ścieszki z png używanego w LoadingBar-ze - uwaga zalecany format png!")
    parser.add_argument("-dc", "--download_config", help="czy pobierać plik konfiguracyjny z serwera?")
    parser.add_argument("-sc", "--serwer_config",
                        help="przechowuje url do serwera z plikiem jsonowy który będzie plikiem konfiguracyjnym")
    parser.add_argument("-d", "--discretizationLoadingBar", type=int, help="określa poziom dyskretyzacji")
    parser.add_argument("-p", "--port", type=int,
                        help="numer portu na który będą wysyłane informacje o udanym pobraniu"),
    args = parser.parse_args()
    for key, value in list(args.__dict__.items()):
        if value is None or value == False:
            # print("usuniete "+ str(key)+ " "+ str(value))
            del args.__dict__[key]
    # print("after command line"))
    # pprint(args.__dict__))

    if os.path.exists('config.json'):
        config_args = argparse.Namespace()
        try:
            with open('config.json', 'rt') as f:
                config_args = argparse.Namespace()
                config_args.__dict__.update(json.load(f))
                # pprint(config_args)
                config_args.__dict__.update(vars(args))
            for key, value in list(config_args.__dict__.items()):
                if value == "False" or value == "false":
                    config_args.__dict__[key] = False
                elif value == "True" or value == "true":
                    config_args.__dict__[key] = True
                if key == "__comment__":
                    del config_args.__dict__[key]
        except JSONDecodeError as e:
            print("Sprawdź czy plik config.json nie jest pusty")
            print("Jeśli tak, możliwe że rozruch umożliwi skopiowanie config.json.example jako config.json")
            traceback.print_exc()
    else:
        print(
            "Brak pliku konfiguracyjnego - jeśli żadnego nie posiadasz prośba o skopiowanie \n config.json.example i nazwanie owej kopii config.json")

    if config_args.debug_logslideshow:
        print("Aktywacja trybu debug")
        logging.root.setLevel(logging.DEBUG)
    return config_args


class Ui_MainWindow(object):

    def __init__(self, args):
        logging.debug("UI_MainWindow __init__")

        #tryb pobierania
        self.mode_download = args.mode_download #wifi, gsm lub both
        #parametry GSM
        self.path_gsm = args.path_gsm # np. "/dev/ttyUSB0"
        self.baudrate = args.baudrate
        #
        self.lab_loadingbBar = None  # label na loadingbara
        self.lab_slajd = None  # label na widget/mape
        self.numerZdjecia = 0  # zmienna wskazuje nam numer obrazka który obecnie jest wyświetlany
        self.widthWindow = 925
        self.heightWindow = 810
        self.sizeOfLoadingBar = int(args.sizeOfLoadingBar)
        self.ustawienieCzasowTimerow(args.timeForDownloader,args.timeForPicture)
        self.sizeOfLoadingBar = int(args.sizeOfLoadingBar)
        self.discretizationLoadingBar = int(args.discretizationLoadingBar)
        self.MainWindow = None
        self.slajdy = args.zdjeciaSlajd
        self.numerZdjecia = 0
        self.pasekpng = args.pasekpng[0]
        self.wypelnienie = 0
        self.flag_UpdatePrzedChwilaConfiga = False
        self.liczbaPrzerwanychPolaczen = 0
        self.workdirectory = args.workdirectory
        self.download_config = args.download_config #True/False
        self.serwer_config = args.serwer_config
        self.segmentationTimeLoadingBar = 1000  # czas w mikrosekundach jednego segmentu loadingBar
        self.port = args.port

        # timery
        self.timerDownloader = None
        self.timerFrame = None
        self.timerResetInnych = None

    def ustawienieCzasowTimerow(self, timeForDownloader, timeForPicture):
        self.czasObrazka = int(
            timeForPicture) * 1000  # w milisekundach #bez int - napis zostanie ... wygenerowany 1000 razy
        self.timeForDownloader = int(timeForDownloader) * 1000  # w milisekundach

    def setupUi(self, MainWindow):
        logging.debug("setupUi - inicjalne uruchomienie")
        # glówne okno
        self.mainWindow = MainWindow
        self.mainWindow.setObjectName("MainWindow")
        self.mainWindow.setWindowTitle("MainWindow")
        self.mainWindow.resize(self.widthWindow, self.heightWindow)
        # pasek u góry
        self.lab_loadingBar = QtWidgets.QLabel(self.mainWindow)
        self.setWidthLoadingBar()
        self.lab_loadingBar.setText("")
        self.lab_loadingBar.setScaledContents(True)
        self.lab_loadingBar.setObjectName("lab_loadingBar")
        self.lab_loadingBar.setPixmap(QtGui.QPixmap(self.pasekpng))
        self.lab_loadingBar.setScaledContents(True)
        # mapa i widget
        self.lab_slajd = QtWidgets.QLabel(MainWindow)
        self.lab_slajd.setGeometry(
            QtCore.QRect(0, self.sizeOfLoadingBar, self.widthWindow, self.heightWindow - self.sizeOfLoadingBar))
        self.lab_slajd.setText("")
        self.lab_slajd.setPixmap(QtGui.QPixmap(self.slajdy[self.numerZdjecia]['nazwapng']))
        self.lab_slajd.setScaledContents(True)
        self.lab_slajd.setObjectName("lab_slajd")

        # timery
        self.setTimerDownloadFiles()
        self.setTimerChangeFrame()
        # inicjalne pobranie
        logging.debug("inicjalne pobranie")
        self.downloadFiles()

    def setWidthLoadingBar(self):
        self.lab_loadingBar.setGeometry(
            QtCore.QRect(0, 0, self.wypelnienie * (self.widthWindow / self.discretizationLoadingBar),
                         self.sizeOfLoadingBar))

    def setLabelPicture(self):
        self.lab_slajd.setGeometry(
            QtCore.QRect(0, self.sizeOfLoadingBar, self.widthWindow, (self.heightWindow - self.sizeOfLoadingBar)))

    # uwaga - metoda verify dziala tylko dla png formatu
    def checkPicture(self, picturepng):
        brokenImage = False
        try:
            img = Image.open(picturepng)
            img.verify()
            logging.debug("Poprawny png " + str(picturepng))
            brokenImage = False
        except Exception:
            brokenImage = True
            logging.debug('Błąd przy odczycie zdjęcia ' + str(picturepng))
        except FileExistsError:
            logging.debug("Nie znaleziono pliku: " + str(picturepng))
            brokenImage = True
        return brokenImage

    def changeFrame(self):
        try:
            #logging.debug("metoda changeFrame")
            flagaZmianaZdjecia = False
            flagaZmianaZdjecia = self.changeLoadingBar()
            if flagaZmianaZdjecia == True:
                self.changePicture()
            self.setLabelPicture()
            self.setWidthLoadingBar()
        except Exception as e:
            print("Zlapano błąd przy zmianie obrazka !")
            traceback.print_exc()

    def changePicture(self):
        logging.debug("changePicture Function - numerZdjecia=" + str(self.numerZdjecia))
        try:
            numer = self.numerZdjecia
            # brokenImage=self.checkPicture(self.slajdy[numer]['nazwapng'])
            # if brokenImage == False:

            pixmap = QtGui.QPixmap(self.slajdy[numer]['nazwapng'])
            self.lab_slajd.setPixmap(pixmap)
            # else:
            #    self.lab_slajd.setPixmap(QtGui.QPixmap(str(self.slajdy[numer])+".bkp"))
            #    logging.debug(str(self.slajdy[numer]))
            if (len(self.slajdy) - 1 > numer):
                self.numerZdjecia = self.numerZdjecia + 1
            else:
                self.numerZdjecia = 0
            self.wypelnienie = 0
        except IOError as error:
            print("Wystapil blad przy otwieraniu pliku " + str(self.slajdy[numer]))
        except Exception as error:
            print("wystapil blad przy przemianie zdjecia w changePicture " + str(error))
            numer = self.numerZdjecia = 0

    def changeLoadingBar(self):
        flagaZmianaZdjecia = False
        if self.wypelnienie < self.discretizationLoadingBar:
            self.wypelnienie = self.wypelnienie + 1
            flagaZmianaZdjecia = False
        else:
            self.wypelnienie = 0
            flagaZmianaZdjecia = True
        # logging.debug("changeLoadingBar metoda - Wypelnienie="+str(self.wypelnienie))
        return flagaZmianaZdjecia

    def checkLastModifiedTimePicture(self, slajd):
        czasUtworzenia = ""
        flag_RozneDaty = False
        with urlopen(slajd['url']) as f:
            logging.debug("Uwaga czasy są pokazywane w czasie uniwersalnym (greenwich)")
            czasUtworzenia = dict(f.getheaders())['Last-Modified']
            logging.debug("slajd u nas: " + str(slajd['dataUtworzenia']))
            logging.debug("slajd tam  : " + str(czasUtworzenia))
            logging.debug("czy pobieramy? " + str(flag_RozneDaty))
            if czasUtworzenia == slajd['dataUtworzenia']:
                logging.debug("data zdjecia nie zmieniła się")
                flag_RozneDaty = False
            else:
                slajd['dataUtworzenia'] = czasUtworzenia
                flag_RozneDaty = True
        return flag_RozneDaty

    def checkLastModifiedTimeConfig(self, serwer_config):
        czasUtworzenia = ""
        flag_RozneDaty = False
        with urlopen(serwer_config['url']) as f:
            # logging.debug("Uwaga czasy są pokazywane w czasie uniwersalnym (greenwich)")
            czasUtworzenia = dict(f.getheaders())['Last-Modified']
            # logging.debug("config u nas: "+str(serwer_config['dataUtworzenia']))
            # logging.debug("config tam  : "+str(czasUtworzenia))
            # logging.debug("czy pobieramy? "+str(flag_RozneDaty))
            if czasUtworzenia == serwer_config['dataUtworzenia']:
                # logging.debug("data configu nie zmieniła się")
                flag_RozneDaty = False
            else:
                logging.debug("nowa data configa na serwerze " + str(czasUtworzenia))
                serwer_config['dataUtworzenia'] = czasUtworzenia
                flag_RozneDaty = True
        return flag_RozneDaty

    def createWorkingSlideshowTxt(self):
        os.chdir('/tmp/')
        logging.debug("folder na plik tymczasowy: " + str(os.getcwd()))
        if os.path.isfile('working_slideshow.txt'):
            logging.debug("working_slideshow.txt plik istnieje")
        else:
            try:
                f = open("working_slideshow.txt", "w+")
            except FileNotFoundError:
                logging.debug("Uszkodzony plik lub zła ścieszka")
            logging.debug("stworzono working_slideshow.txt plik")
        os.chdir(self.workdirectory)
        logging.debug("Wracamy do folderu roboczego: " + str(os.getcwd()))

    def downloadFiles(self):
        print("downloadFiles method")
        flagDownloadBroken = True
        flaga_czyCosPobrano = False
        if self.mode_download == "both" or self.mode_download == "wifi":
            if self.flag_UpdatePrzedChwilaConfiga == False:
                logging.debug("----------------------------------------------")
                pprint(self.slajdy)
                logging.debug("downloadFiles")
                flagDownloadBroken = True
                flaga_czyCosPobrano = False
                try:
                    logging.debug("downloadPictures")
                    for slajd in list(self.slajdy):
                        flaga_pobierzZdjecie = False
                        flaga_pobierzZdjecie = self.checkLastModifiedTimePicture(slajd)
                        if flaga_pobierzZdjecie:
                            logging.debug("Przed pobraniem: slajd " + str(slajd['nazwapng']) + str(slajd['dataUtworzenia']))
                            r_slajd = requests.get(slajd['url'], allow_redirects=True)
                            with open(slajd['nazwapng'] + ".download", 'wb') as file_slajd:
                                file_slajd.write(r_slajd.content)
                            # logging.debug("Data utworzenia pliku:"+str(self.get_created_taken()))
                            os.rename(slajd['nazwapng'] + ".download", slajd['nazwapng'])
                            logging.debug("pobrano zdjęcia " + slajd['nazwapng'] + " " + slajd['dataUtworzenia'])
                            flaga_czyCosPobrano = True
                    print("zdjecia po sprawdzeniu")
                    # pprint(self.slajdy)

                    logging.debug("downloadConfig")
                    flaga_pobierzConfig = False
                    if self.download_config == False:
                        print("ustawiona brak pobierania configa z serwera")
                    else:
                        flaga_pobierzConfig = self.checkLastModifiedTimeConfig(self.serwer_config)
                        if flaga_pobierzConfig:
                            logging.debug("Przed pobraniem config " + self.serwer_config['url'] + " " + str(
                                self.serwer_config['dataUtworzenia']))
                            r_serwer_config = requests.get(self.serwer_config['url'], allow_redirects=True)
                            nazwa_zapisanego_configa = 'config.json'
                            with open(nazwa_zapisanego_configa, 'wb') as file_json:
                                file_json.write(r_serwer_config.content)
                            logging.debug("pobrano zapisany config o nazwie: " + str(nazwa_zapisanego_configa))
                            self.aktualizacjaConfigowychParametrow()

                            flaga_czyCosPobrano = True
                    if flaga_czyCosPobrano == True:
                        ###### WYSŁANIE SATUSU NA SERVER CZUJNIKI MIEJSKIE ZE WSZYSTKO JEST OK ########
                        session = Session()
                        # HEAD requests ask for *just* the headers, which is all you need to grab the
                        # session cookie
                        print("pobieranie w slideshow działa")
                        response = session.post(
                            url='http://czujnikimiejskie.pl/apipost/add/measurement',
                            data={"sn": str(self.port), "a": "1", "w": "0", "z": "0"},
                        )
                        print(response.text)
                        self.createWorkingSlideshowTxt()
                    flagDownloadBroken = False
                except requests.exceptions.RequestException as error:
                    flagDownloadBroken = True
                    print("Wystąpił problem z połączeniem:" + str(error))
                    traceback.print_exc()
                except Exception as error:
                    flagDownloadBroken = True
                    print("Wystąpił problem z połączeniem:" + str(error))
                    print("Wykryto bład : " + str(error))
                    traceback.print_exc()
            else:  # self.flag_UpdatePrzedChwilaConfiga==True:
                logging.debug("przed chwila zmieniono dane configa - pobieranie wstrzymane do kolejnej iteracji pobierania")
                self.flag_UpdatePrzedChwilaConfiga = False
            self.aktualnyStanZmiennychConfigowych()
        if flagDownloadBroken == True and (self.mode_download == "both" or self.mode_download == "gsm"):
            #logging.debug("Przed pobraniem config " + str(self.serwer_config['url']) + str(" ") + str(self.serwer_config['dataUtworzenia']))
            self.download_via_sim800L()
        logging.debug("koniec downloadFiles")

    def download_via_sim800L(self):
        gsm_slideshow = GsmSlideshow(path=self.path_gsm)
        logging.debug(str(self.serwer_config))
        if self.download_config == True:
            gsm_slideshow.download_file(nazwa="config.json", extension="json"
                                        , url=self.serwer_config['url']
                                        , sleep_to_read_bytes=30)
        for slajd in list(self.slajdy):
            logging.debug(self.slajdy)
            gsm_slideshow.download_file(nazwa=slajd['nazwapng'], extension="png"
                                        , url=slajd['url']
                                        , sleep_to_read_bytes=30)
        #gsm_slideshow.download_file()

    def updateZmiennych(self, config_args):
        logging.debug("updateZmiennych")
        self.ustawienieCzasowTimerow(config_args.timeForDownloader, config_args.timeForPicture)
        self.sizeOfLoadingBar = config_args.sizeOfLoadingBar
        self.slajdy = config_args.zdjeciaSlajd
        self.pasek = config_args.pasekpng[0]
        self.discretizationLoadingBar = config_args.discretizationLoadingBar
        self.port = config_args.port

    def aktualnyStanZmiennychConfigowych(self):
        print("---------stan-zmiennych-configowych---------")
        print("sizeOfLoadingBar      :" + str(self.sizeOfLoadingBar))
        print("pasek                 :" + str(self.pasekpng))
        print("czasObrazka           :" + str(self.czasObrazka))
        print("timeForDownloader     :" + str(self.timeForDownloader))
        print("discretizationLoadingBar:" + str(self.discretizationLoadingBar))
        print("port                  :" + str(self.port))
        print("slajdy          :" + str(self.slajdy))

    def aktualizacjaConfigowychParametrow(self):
        print("----*****************----")
        logging.debug("aktualizacjaConfigowychParametrow")
        if os.path.exists('config.json'):
            config_args = argparse.Namespace()
            # zczytuje configa bo sie zmienił
            with open('config.json', 'rt') as f:
                config_args = argparse.Namespace()
                config_args.__dict__.update(json.load(f))
                # pprint(config_args)
            for key, value in list(config_args.__dict__.items()):
                if value == "False" or value == "false":
                    config_args.__dict__[key] = False
                elif value == "True" or value == "true":
                    config_args.__dict__[key] = True
                if key == "__comment__":
                    del config_args.__dict__[key]
            logging.debug("zczytane zmienne")
            pprint(config_args)

            # ustawiam zmienne z nowego configa, ktorych zmiana jest istotna
            self.updateZmiennych(config_args)

            # resetuje timery
            logging.debug("resetuje timery")
            self.stopTimerDownloadFiles()
            self.stopTimerChangeFrame()
            self.setTimerDownloadFiles()
            self.setTimerChangeFrame()
            self.flag_UpdatePrzedChwilaConfiga = True
        else:
            print("Brak pliku konfiguracyjnego - jeśli żadnego nie posiadasz prośba o skopiowanie \n     "
                  "config.json.example i nazwanie owej kopii config.json")

    def setTimerChangeFrame(self):
        logging.debug("setTimerChangeFrame")
        self.timerFrame = QtCore.QTimer()
        self.timerFrame.timeout.connect(self.changeFrame)
        timeToChangePicture = int(floor(int(self.czasObrazka)))
        logging.debug("czasObrazka:" + str(timeToChangePicture) + " ms")
        self.segmentationTimeLoadingBar = int(floor(int(self.czasObrazka) / self.discretizationLoadingBar))
        self.timerFrame.setInterval(self.segmentationTimeLoadingBar)
        logging.debug("timeToChange: " + str(self.segmentationTimeLoadingBar) + " ms")
        self.timerFrame.start()

    def stopTimerChangeFrame(self):
        self.timerFrame.stop()
        print("ahoj stopuje timerFrame")

    def setTimerDownloadFiles(self):
        logging.debug("setTimerDownloadFiles")
        self.timerDownloader = QtCore.QTimer()
        self.timerDownloader.timeout.connect(self.downloadFiles)
        timeForDownloader = self.timeForDownloader
        logging.debug("czasUruchomieniaPobrania: " + str(timeForDownloader) + " minisekund")
        self.timerDownloader.setInterval(timeForDownloader)
        self.timerDownloader.start()

    def stopTimerDownloadFiles(self):
        self.timerDownloader.stop()
        print("stopuje timerDownloader")

    def setSizeWindow(self):
        self.widthWindow = self.mainWindow.frameGeometry().width()
        self.heightWindow = self.mainWindow.frameGeometry().height()
        logging.debug("widthWindow :" + str(self.widthWindow))
        logging.debug("heightWindow :" + str(self.heightWindow))
        self.setLabelPicture()
        self.setWidthLoadingBar()


class Window(QtWidgets.QMainWindow):
    resized = QtCore.pyqtSignal()

    def __init__(self, args):
        super(Window, self).__init__(parent=None)
        self.ui = Ui_MainWindow(args)
        self.ui.setupUi(self)
        self.resized.connect(self.resizeEventFunction)
        if args.fullScreenSlideshow:
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
        if event.key() == Qt.Key_Space:
            logging.debug("Klawisz Spacja został wciśniety")
            if self.isFullScreen() == False:
                self.showFullScreen()
                event.accept()
                logging.debug("włączono tryb pełnoekranowy")


if __name__ == "__main__":
    obecny_folder = os.getcwd()
    logging.debug("początkowy folder wykonywania:" + str(obecny_folder))
    args = def_params()
    logging.debug(pformat(args))
    #ustawienoe folderu roboczego projektu, na podstawie parametru wejściowego
    os.chdir(args.workdirectory)
    obecny_folder = os.getcwd()
    logging.debug("obecny folder roboczy:" + str(obecny_folder))
    # odpalenie aplikacji
    app = QtWidgets.QApplication(sys.argv)
    w = Window(args)
    w.show()
    sys.exit(app.exec_())
