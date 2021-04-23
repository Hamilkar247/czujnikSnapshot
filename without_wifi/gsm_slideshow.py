import logging
import traceback

from usim800_slideshow.usim800 import sim800_slideshow


class GsmSlideshow:
    def __init__(self, path):
        try:
            logging.debug
            self.gsm = sim800_slideshow(baudrate=115200, path=path)
            self.gsm.requests._APN = "internet"
            self.r = None
        except Exception as e:
            print("Wystąpił błąd przy próbie otwarcia portu GsmSlideshow - możliwe że inny program używa już podanego portu!")
            traceback.print_exc()

    def download_file(self, nazwa, extension, url, sleep_to_read_bytes):
        try:
            nazwa_pliku = nazwa
            self.gsm.requests.getFile(url=url, extension=extension,
                                      sleep_to_read_bytes=sleep_to_read_bytes, nameOfFile=nazwa_pliku)
        except Exception as e:
            print("Niestety jest błąd - wyrzuciło download_file w GsmSlideshow")
            print(f"{e}")
            return False
        logging.debug("koniec pliku")
        return True
