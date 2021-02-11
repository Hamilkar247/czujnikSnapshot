#!/bin/bash

#zczytuje folder roboczy
WD=/home/matball/Projects/czujnikSnapshot
cd "$WD"
timeToSleep="$(jq '.timeToCheckSlideshow' config.json)"
rebootActivate="$(jq -r '.rebootActivate' config.json)"
if [[ "$timeToSleep" == "" ]]
 then
   timeToSleep=5
   echo "ahjo nie ma zmiennej timeToSleep"
   exit
fi

sleep 5 #czas by slideshow.py miał czas zczytać configa etc
var_nofound=0
while true
do
  echo "sprawdzam czy plik working_slideshow.txt istnieje"
  if [ -f "/tmp/working_slideshow.txt" ]
  then
    echo "usuwam plik working_slideshow.txt"
    rm working_slideshow.txt
    var_nofound=0
  else
    echo "nie znalazłem pliku"
    var_nofound=$(( var_nofound+1 ))
  fi
  echo "var_nofound=$var_nofound"
  if [[ "$var_nofound" -eq "3" ]] #is a greater than or equal
    then
      echo "nie znaleziono po raz trzeci pliku"
      var_nofound=$(( var_nofound+1 ))
      echo "Wykonuje 'systemctl start stop' na serwisie 'NetworkManager.service'"
      systemctl stop NetworkManager.service
      systemctl start NetworkManager.service
      #reboot
  fi
  if [[ "$var_nofound" -eq "5" ]]
    then
      echo "nie znaleziono pliku po raz piąty - resetuje slideshow"
      echo "Stopuje i potem ponownie uruchomiam serwis 'slideshow.service'"
      systemctl stop slideshow.service
      systemctl start slideshow.service
      var_nofound=$(( var_nofound+1 ))
  fi
  if [[ "$var_nofound" -ge "7" ]]
    then
      if [[ "$rebootActivate" -eq "true" ]]
        then
        echo "nie znaleziono pliku po raz siódmy - dokonuje całego urządzenia"
        sleep 1
        reboot
      else
        var_nofound="0"
      fi
  fi
  sleep "$timeToSleep" # czas w sekundach
done
