import logging
import traceback
from pprint import pprint

import pytest
from without_wifi import FtpSlideshow
import os

s1= """
AT+FTPLIST=2,1024

+FTPLIST: 2,444
drwxrwxr-x    2 1979163    www-data         4096 May  6 14:37 .
drwxr-xr-x    3 1979163    www-data         4096 May  6 14:37 ..
-rw-rw-r--    1 1979163    www-data       850023 May  7 14:19 mapaKozienice.png
-rw-rw-r--    1 1979163    www-data           45 May  6 12:10 post.json
-rw-rw-r--    1 1979163    www-data           45 May  5 18:07 testowo.json
-rw-rw-r--    1 1979163    www-data       204387 May  5 16:45 widgetKozienice.png

OK"""


s2="""
drwxrwxr-x    2 1979163    www-data         4096 May  6 14:37 .
drwxr-xr-x    3 1979163    www-data         4096 May  6 14:37 ..
-rw-rw-r--    1 1979163    www-data       850023 May  7 14:19 mapaKozienice.png
-rw-rw-r--    1 1979163    www-data           45 May  6 12:10 post.json
-rw-rw-r--    1 1979163    www-data           45 May  5 18:07 testowo.json
-rw-rw-r--    1 1979163    www-data       204387 May  5 16:45 widgetKozienice.png
"""


def delete_redundant_lines():
    text_to_parse=[]
    lines=s1.lstrip().split('\n')
    for number in range(len(lines)-1):
        pprint(lines[number].split())
        print(f"lines {number} {lines[number].split()}")
        if len(lines[number].split())-1 == 8:
            print("dodaje linie do zbioru")
            text_to_parse.append(lines[number])
    return text_to_parse


def parse_metadata_file(zdjecie, rozmiar_pliku, data_zdjecia):
    text_to_parse=delete_redundant_lines()
    try:
        #lstrip usuwa puste znaki na początku (ale nie na końcu linii)
        lines = text_to_parse
        pprint(lines)
        pprint("pierwsza linia" + lines[0])
        print("ahjo")
        for number in range(len(lines)-1):
            columns = lines[number].split()
            links = columns[0]
            owner = columns[2]
            group = columns[3]
            size = columns[4]
            date = columns[5]+" "+columns[6]+" "+columns[7]
            Name = columns[-1]
            if zdjecie == Name:
                print(zdjecie)
                print(f"data {date} vs {data_zdjecia}")
                print(f"rozmiar pliku: {size} vs {rozmiar_pliku}")
                print(f"nazwa pliku: {Name} vs {zdjecie}")
                if rozmiar_pliku == size and data_zdjecia == date:
                    return True
                print("\n")
        return False
    except Exception as e:
        print(f"blad przy parsowaniu {e}")
        traceback.print_exc()
        return False


def test_metadata_from_server_mapaKozienice():
    assert parse_metadata_file(zdjecie="mapaKozienice.png",
                               rozmiar_pliku="850023",
                               data_zdjecia="May 7 14:19")


def test_metadata_from_server_widgetKozienice():
    assert parse_metadata_file(zdjecie="widgetKozienice.png",
                               rozmiar_pliku="204387",
                               data_zdjecia="May 5 16:45")
