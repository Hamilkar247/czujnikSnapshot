#!/bin/python3
import logging
import argparse
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options
import os
import time
import datetime

display = Display(visible=0, size=(1920, 1200))
display.start()

args = []

def def_params():
    parser = argparse.ArgumentParser(
            description="Description to fill"
    )
    parser.add_argument("-l", "--loghami", action='store_true', help="set debug")
    args = parser.parse_args()
    if args.loghami:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug("Only shown in debug mode")
        print("args:" + str(args))
    return args

def def_environment():
    path_to_dir = os.path.dirname(os.path.realpth(__file__))
    os.environ["PATH"] += os.pathsep + path_to_dir

def czujnikiSnapshot():
    logging.debug("czujnikiSnapshot!")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    url='http://czujnikimiejskie.pl/public/kozienice/'
    driver.get(url)
    screenshot = driver.save_screenshot('kolno_map.png')
    driver.quit()

def main():
    args=def_params()
    path_to_dir = os.path.dirname(os.path.realpath(__file__))
    print("Ścieszka do folderu"+path_to_dir)
    os.environ["PATH"] += os.pathsep + path_to_dir
    czujnikiSnapshot()


if __name__ == "__main__":
    main()
