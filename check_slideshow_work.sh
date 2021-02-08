#!/bin/bash

#zczytuje folder roboczy
WD=$(sed 's/.*"workdirectory": "\(.*\)".*/\1/;t;d' config.json)

echo "$WD"
cd "$WD" || return

while true
do
  echo "sprawdzam czy plik working_slideshow.txt istnieje"
  if [ -f "$WD""/working_slideshow.txt" ]
  then
    echo "usuwam plik working_slideshow.txt"
  else
    echo "nie znalazłem pliku"
  fi
  sleep 3 # czas w sekundach
done
