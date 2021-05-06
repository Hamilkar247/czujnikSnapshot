import logging
import os
import sys

import pytest
from without_wifi import FtpSlideshow


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


def post_via_sim800L():
    try:
        tekst_do_przeslania = "ooorety#"  # '{"sn": "3005", "a": "1", "w": "0", "z": "0" }'
        nazwa_pliku = "testowo.json"
        ftp_slideshow = FtpSlideshow(path="/dev/ttyUSB0", baudrate="115200")

        return ftp_slideshow.post_file(put_name_file=nazwa_pliku, get_name_file=nazwa_pliku,
                                       server_ip="37.48.70.196",
                                       put_path_file="/hamilkar.cba.pl/",
                                       get_path_file="/hamilkar.cba.pl/", nickname="hamilkar", password="Hamilkar0",
                                       text_to_post=tekst_do_przeslania)
    except Exception as e:
        return False


@pytest.mark.usefixtures("chdir_root_folder")
def test_post_via_sim800L():
    assert post_via_sim800L()
