# -*- encoding: utf-8 -*-
import requests
import os
import time
from requests import Session
while True:
    try:
        url_widget = 'http://134.122.69.201/widgetKozienice/'
        r_widget = requests.get(url_widget, allow_redirects=True)
        with open('widget.jpg', 'wb') as file_wiedget:
            file_wiedget.write(r_widget.content)
        url_map = 'http://134.122.69.201/mapaKozienice/'
        r_map = requests.get(url_map, allow_redirects=True)
        with open('mapa.jpg', 'wb') as file_map:
            file_map.write(r_map.content)
        ###### WYSŁANIE SATUSU NA SERVER CZUJNIKI MIEJSKIE ZE WSZYSTKO JEST OK ########
        session = Session()
        # HEAD requests ask for *just* the headers, which is all you need to grab the
        # session cookie
        stat_kweb = os.system('systemctl is-active --quiet kiosk_kweb.service')
        stat_downloader = os.system('systemctl is-active --quiet downloader_kiosk.service')
        print("Status kweb:")
        print(stat_kweb)
        print("Status downloader")
        print(stat_downloader)
        if (stat_kweb==0 and stat_downloader==0):
                print("Kweb i downloader działają")
                response = session.post(
                            url='http://czujnikimiejskie.pl/apipost/add/measurement',
                            data={"sn":"3004","a":"1","w":"0","z":"0"},
                )
                print(response.text)
        if stat_kweb!=0:
                os.system('sudo systemctl stop kiosk_kweb.service')
                os.system('sudo systemctl start kiosk_kweb.service')
    except Exception as inst:
        print("Wykryto bład : "+str(inst))
    time.sleep(600)
