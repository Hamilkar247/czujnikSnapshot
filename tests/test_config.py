import logging
import os
from pathlib import Path
import argparse
import pytest
from dotenv import load_dotenv

from slideshow import def_params


@pytest.fixture()
def chdir_root_folder_project():
    logging.root.setLevel(logging.DEBUG)
    load_dotenv()
    env_path = Path("..")
    load_dotenv(dotenv_path=env_path)
    os.chdir(os.getenv("ROOT_FOLDER_PROJECT"))


@pytest.mark.usefixtures("chdir_root_folder_project")
def test_config_open_and_read_variable():
    print(os.getcwd())
    name_config="config.json"
    arguments = def_params(name_config)
    if arguments is None:
        print("Nie udało się odczyt pliku" + name_config)
        assert False
    else:
        assert True


@pytest.mark.usefixtures("chdir_root_folder_project")
def test_config_example_open_and_read_variable():
    print(os.getcwd())
    name_config="config.json.example"
    arguments = def_params(name_config)
    if arguments is None:
        print("Nie udał się odczyt pliku " + name_config)
        assert False
    else:
        assert True
