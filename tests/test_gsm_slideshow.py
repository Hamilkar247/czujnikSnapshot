import hashlib
import logging

import pytest
from dotenv import load_dotenv
from pathlib import Path
import os

from without_wifi.gsm_slideshow import GsmSlideshow


@pytest.fixture()
def chdir_root_folder_project():
    load_dotenv()
    env_path = Path("..")
    load_dotenv(dotenv_path=env_path)
    os.chdir(os.getenv("ROOT_FOLDER_PROJECT"))


def delete_file(name_png):
    try:
        os.remove(name_png)
        print("poprawnie usunieto pobrany plik testowy")
        return True
    except Exception as e:
        print("Nie znaleziono pliku "+name_png)
        return False


@pytest.mark.usefixtures("chdir_root_folder_project")
def test_gsm_slideshow_blank_without_redirect_link():
    name_file="blank.test.png"
    extension="png"
    url="http://134.122.69.201/blank.png"
    sleep_to_read_bytes=4
    logging.basicConfig(level=logging.DEBUG, force=True)
    #na sztywno
    paths=["/dev/ttyUSB0", "/dev/ttyUSB1"]
    gsm_slideshow = None
    for gsm_path in paths:
        try:
            gsm_slideshow = GsmSlideshow(path=gsm_path)
        except Exception as e:
            print("zla scieszka - przechodzimy do kolejnego path-a")
            continue
        break
    if gsm_slideshow is None:
        assert False

    if gsm_slideshow.download_file(nazwa=name_file, extension=extension,
                                       url=url, sleep_to_read_bytes=sleep_to_read_bytes):
        assert delete_file(name_file)
    else:
        assert False


@pytest.mark.usefixtures("chdir_root_folder_project")
def test_gsm_slideshow_widget_with_redirect_link():
    name_file = "widgetKozienice.test.png"
    extension = "png"
    url = "http://134.122.69.201/widgetKozienice/"
    sleep_to_read_bytes = 30
    logging.basicConfig(level=logging.DEBUG, force=True)
    # na sztywno
    paths = ["/dev/ttyUSB0", "/dev/ttyUSB1"]
    gsm_slideshow = None
    for gsm_path in paths:
        try:
            gsm_slideshow = GsmSlideshow(path=gsm_path)
        except Exception as e:
            print("zla scieszka - przechodzimy do kolejnego path-a")
            continue
        break
    if gsm_slideshow is None:
        assert False
#
    if gsm_slideshow.download_file(nazwa=name_file, extension=extension,
                                   url=url, sleep_to_read_bytes=sleep_to_read_bytes):
        delete_file(name_file)
        assert True
    else:
        assert False


@pytest.mark.usefixtures("chdir_root_folder_project")
def test_gsm_slideshow_config_with_redirect_link():
    name_file="config.test.json"
    extension="json"
    url="https://134.122.69.201/configKozienice/"
    sleep_to_read_bytes=10
    logging.basicConfig(level=logging.DEBUG, force=True)
    #na sztywno
    paths=["/dev/ttyUSB0", "/dev/ttyUSB1"]
    gsm_slideshow = None
    for gsm_path in paths:
        try:
            gsm_slideshow = GsmSlideshow(path=gsm_path)
        except Exception as e:
            print("zla scieszka - przechodzimy do kolejnego path-a")
            continue
        break

    if gsm_slideshow is None:
        assert False

    if gsm_slideshow.download_file(nazwa=name_file, extension=extension,
                                       url=url, sleep_to_read_bytes=sleep_to_read_bytes):
        delete_file(name_file)
        assert True
    else:
        assert False
