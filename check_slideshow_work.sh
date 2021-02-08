#!/bin/bash

#zczytuje folder roboczy
WD=$(sed 's/.*"workdirectory": "\(.*\)".*/\1/;t;d' config.json)
timeToSleep=$(sed 's/.*"timeToCheckSlideshow": \(.*\),/\1/;t;d' config.json)
if [[ "$timeToSleep" == "" ]]
 then
   timeToSleep=5
   echo "ahjo nie ma zmiennej timeToSleep"
   exit
fi

echo "$WD"
cd "$WD" || return

sleep 5 #czas by slideshow.py miał czas zczytać configa etc
while true
do
  echo "sprawdzam czy plik working_slideshow.txt istnieje"
  if [ -f "$WD""/working_slideshow.txt" ]
  then
    echo "usuwam plik working_slideshow.txt"
    rm working_slideshow.txt
  else
    echo "nie znalazłem pliku"
  fi
  sleep "$timeToSleep" # czas w sekundach
done
