=== flagi debug

debug_logslideshow - flaga debug programu slideshow.py

=== check_slideshow_work.sh 

skrypt bashowy (a właściwie i checkSlideshow.service który uruchamia ten program) sprawdza czy
istnieje w /tmp/ (absolutna ścieszka!) plik working_slideshow.txt. Sprawdza to co czas określany jako timeToCheckSlideshow. Jeśli plik zostanie znaleziony - usuwa go i zasypia na czas timeToCheckSlideshow
- kiedy 3 razy nie znajdziemy pliku - resetujemy NetworkManager.service
- kiedy 5 razy nie znajdziemy pliku - resetujemy serwis slideshow.service - co spowoduje restart slideshow.py ( a więc wyświetlanego programu python ).
- kiedy 7 razy nie znajdziemy pliku - dokonujemy reboot raspberki

=== ZMIENNE używane w check_slideshow_work.sh
timeToCheckSlideshow:
- czas co jaki się aktywuje skrypt check_slideshow_work.sh 
rebootActivate:
- ustawione domyślnie na true - jeśli wpiszemy false głównie na potrzeby testów - nie będzie reboota

=== slideshow.py

skrypt pythonowy (a własciwie slideshow.service), odpowiadający za uruchomienia PyQt5 i wyświetlania plików pobieranych z url. Ważną kwestią jest to, że w przypadku poprawnego pobrania tworzony w '/tmp/' jest plik 'working_slideshow.txt' gdyby go nie było. w przypadku zawieszenia programu (np. przerwanie połączenia w czasie pobierania zdjęcia) serwis sprawdzający checkSlideshow.service wymusi zresetowanie slideshow.py

=== ZMIENNE używane w slideshow.py
timeForPicture:
- odpowiada za czas wyświetlenia każdego z slajdu - czas podajemy w sekundach
timeForDownloader:
- odpowiada za czas po jakim następuje próba pobranie slajdów z serwera
fullScreenSlideshow:
- jeśli true program wypelnia całą dostepną przestrzeń ekranu
sizeOfLoadingBar:
- rozmiar paska ładowania/loadingbara
workdirectory:
- ścieszka do folderu w którym zawarte są zdjęcia i pliki
serwer_config:
- http do strony z której możemy pobrać aktualny plik config.json
pasekpng:
- plik png używany jako grafika loadingbara/paskaładowania
zdjeciaSlajd:
- zawarte w nim podzbiory odpowiadają za wyświetlane w programie slajdy.

przykład
nazwa png - nazwa pod jaką zostaną zapisane zdjęcia
url - link z którego zostanie podjęta próba pobrania - uwaga url z prefixem https
może powodować problemy
      "zdjeciaSlajd": [
           {
               "nazwapng": "mapaKolno.png",
               "url"     : "http://134.122.69.201/mapaKolno/"
           },
           {
               "nazwapng": "widgetKolno.png",
               "url"     : "http://134.122.69.201/widgetKolno/"
           }
      ]

UWAGI:
parametry liczbowe muszą mieć wartość bez cudzysłowiów !
parametry przełącznikowe (działa, nie działa) muszą być w formie
"true" - cudzysłowia istotnie lub "false"
parametry "True" lub "TRUE" mogą być błedogenne

zdjeciaSlajd - url podaje w przykladzie jako http bo https powoduje czasem brak połączenia
ale wynika to raczej z ustawien raspberki i braku certyfikatu na serwerze
Przykładowy plik konfiguracyjny

{
  "__comment__": "ustawienia debug programów",
      "debug_logslideshow" : "true",
  "__comment__": "zmienne używane w check_slideshow_work",
      "timeToCheckSlideshow": 80,
      "__comment__": "reboot będzie wykonany po 7 iteracjach braku reakcji",
      "rebootActivate":"true",
  "__comment__": "zmienne używane w slideshow - zmienne czasowe podane w sekundach",
      "timeForPicture": 10,
      "timeForDownloader": 60,
      "fullScreenSlideshow": "true",
      "sizeOfLoadingBar": 10,
      "workdirectory": "/home/matball/Projects/czujnikSnapshot",
  "__comment__": "url skąd updatujemy plik config.json",
      "serwer_config": "http://134.122.69.201/config/kiosk/config.json",
  "__comment__": "rubryka na zdjęcia - pierwsze nazwa zdjęcia, drugi url skąd updatujemy",
      "pasekpng": ["kwadrat.png", ""],
      "__comment__": "uwaga - danie w url https może spowodować puste zdjecie",
      "zdjeciaSlajd": [
           {
               "nazwapng": "mapaKozienice.png",
               "url"     : "http://134.122.69.201/mapaKozienice/"
           },
           {
               "nazwapng": "widgetKozienice.png",
               "url"     : "http://134.122.69.201/widgetKozienice/"
           },
           {
               "nazwapng": "mapaPiaseczno.png",
               "url"     : "http://134.122.69.201/mapaPiaseczno/"
           },
           {
               "nazwapng": "widgetPiaseczno.png",
               "url"     : "http://134.122.69.201/widgetPiaseczno/"
           },
           {
               "nazwapng": "mapaKolno.png",
               "url"     : "http://134.122.69.201/mapaKolno/"
           },
           {
               "nazwapng": "widgetKolno.png",
               "url"     : "http://134.122.69.201/widgetKolno/"
           }
      ]
}

