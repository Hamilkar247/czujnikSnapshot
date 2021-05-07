import logging
from pprint import pprint

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


def get_files_metadata(put_path_file):
    logging.debug("get_files_data")
    try:
        ftp_slideshow = FtpSlideshow(path="/dev/ttyUSB0", baudrate="115200")
        metadata=ftp_slideshow.get_files_metadata(
                                            put_path_file=put_path_file,
                                            server_ip="37.48.70.196",
                                            nickname="hamilkar",
                                            password="Hamilkar0")
        print("ahoj !")
        pprint(str(metadata))
        f = open("metadata_from_server.txt", "wb")
        f.write(metadata)
        f.close()
        if metadata is None:
            return False
        else:
            return True
    except Exception as e:
        return False


@pytest.mark.usefixtures('chdir_root_folder')
def test_check_metadata_files():
    assert get_files_metadata("/hamilkar.cba.pl/Kozienice/")
