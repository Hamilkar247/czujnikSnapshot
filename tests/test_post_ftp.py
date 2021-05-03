import logging
import os
import pytest
from without_wifi import FtpSlideshow


def concatenate_list_data(list):
    #print(list)
    result = ''
    for element in list:
        if element != "":
            result += "/" + element
    return result


@pytest.fixture()
def chdir_root_folder():
    path=os.getcwd()
    print(path.split("/")[-1])
    print(path.split("/")[-2])
    if path.split("/")[-1] == "slideshow":
        print("ok, jesteś w root folderze projektu")
    if path.split("/")[-2] == "slideshow":
        print("ok folder wyżej jest root folderem")
        print(path.split("/")[0:-1])
        root_folder=concatenate_list_data(path.split("/")[0:-1])
        print(root_folder)
        os.chdir(root_folder)


def post_via_sim800L():
    ftp_slideshow = FtpSlideshow(path="/dev/ttyUSB0")
    ftp_slideshow.post_file(name_file="o_moj_boze.json", server_ip="37.48.70.196"
                            , path_file="/hamilkar.cba.pl/orety/"
                            , nickname="hamilkar", password="Hamilkar0"
                            , text_to_post='{"sn": "3005", "a": "1", "w": "0", "z": "0" }')


@pytest.mark.usefixtures("chdir_root_folder")
def test_post_via_sim800L():
    print("test")
