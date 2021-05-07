import logging

import pytest
from without_wifi import FtpSlideshow
import os


def concatenate_list_data(list):
    # print(list)
    result = ''
    for element in list:
        if element != "":
            result += "/" + element
    return result


@pytest.fixture()
def chdir_root_folder():
    path = os.getcwd()
    print(path.split("/")[-1])
    print(path.split("/")[-2])
    if path.split("/")[-1] == "slideshow":
        print("ok, jesteś w root folderze projektu")
    if path.split("/")[-2] == "slideshow":
        print("ok folder wyżej jest root folderem")
        print(path.split("/")[0:-1])
        root_folder = concatenate_list_data(path.split("/")[0:-1])
        print(root_folder)
        os.chdir(root_folder)


def get_picture_via_sim800L(nazwa_zdjecia):
    logging.debug("get_picture_via_sim800 - ahjo!")
    try:
        ftp_slideshow = FtpSlideshow(path="/dev/ttyUSB0", baudrate="115200")
        return ftp_slideshow.get_file(extension="png", get_name_file=nazwa_zdjecia,
                                      server_ip="37.48.70.196",
                                      get_path_file="/hamilkar.cba.pl/Kozienice/",
                                      nickname="hamilkar",
                                      password="Hamilkar0")
    except Exception as e:
        return False


@pytest.mark.usefixtures("chdir_root_folder")
def test_ftp_get_picture():
    assert get_picture_via_sim800L(nazwa_zdjecia='mapaKozienice.png')


@pytest.mark.usefixtures("chdir_root_folder")
def test_ftp_get_picture():
    assert get_picture_via_sim800L(nazwa_zdjecia='widgetKozienice.png')