import logging
import traceback

from usim800_slideshow.usim800 import sim800_slideshow
from usim800_slideshow.usim800.usim800_slideshow import ftp_slideshow


class WithoutWifi:
    def __init__(self, path):
        try:
            logging.debug("without wifi")
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


class FtpSlideshow:

    def __init__(self, path, baudrate):
        try:
            logging.debug("ftp slideshow")
            self.ftp = ftp_slideshow(baudrate=115200, path=path)
            #self.ftp.request_ftp._APN =
        except Exception as e:
            print("Wystąpił błąd przy próbie otwarcia portu Ftplideshow - możliwe że inny program używa już podanego portu!")
            traceback.print_exc()

    def get_file(self, APN="internet",extension="png", get_name_file="widget.png", server_ip="37.48.70,196", port=21, mode=0,
                 get_path_file="/", nickname="qaz", password="zxc"):
        logging.debug("get_file <-- FtpSlideshow ")
        try:
            self.ftp.request_ftp.getFile(APN=APN, server_ip=server_ip, port=21, mode=0,
                                         get_name_file=get_name_file, get_path_file=get_path_file
                                         , nickname=nickname, password=password)
        except Exception as e:
            print("Niestety - nie udało się wysłać wiadomości na serwer")
            print(f"{e}")
            return False
        return True

    def post_file(self, APN="internet", server_ip="37.48.70.196", port=21, mode=0,
                  put_name_file="hami.json", get_name_file="hami.json",
                  put_path_file="/hamilkar.cba.pl/myhero/",
                  get_path_file="/",
                  nickname="hamilkar", password="Hamilkar0",
                  text_to_post='{"sn": "3005", "a": "1", "w": "0", "z": "0" }'):
        try:
            self.ftp.request_ftp.postFile(APN=APN, server_ip=server_ip, port=port,
                                          mode=mode,
                                          put_name_file=put_name_file,
                                          get_name_file=get_name_file,
                                          put_path_file=put_path_file,
                                          get_path_file=get_path_file,
                                          nickname=nickname, password=password,
                                          text_to_post=text_to_post)
        except Exception as e:
            print("Niestety - nie udało się wysłać wiadomości na serwer")
            print(f"{e}")
            return False
        logging.debug("koniec pliku ")
        return True