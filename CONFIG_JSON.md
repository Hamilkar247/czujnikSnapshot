version - wersja pliku konfiguracyjnego (od tego mają w załozeniu zalezec zawarte atrybuty

debug_logslideshow - flaga debug programu.
debug_logusim800 - ustawienie wyświetlenia logów dla usim800_slideshow

path_gsm - ścieszka gsm
use_gsm - czy używać gsm w programie
baudrate - z jaką szybkością pobierać dane

timeForPicture - odpowiada za czas wyświetlenia każdego z slajdu - czas podajemy w sekundach
timeForDownloader - odpowiada za czas po jakim następuje próba pobranie slajdów z serwera
fullScreenSlideshow - jeśli true program wypelnia całą dostepną przestrzeń
sizeOfLoadingBar - rozmiar paska ładowania/loadingbara
workdirectory - ścieszka do folderu w którym zawarte są zdjęcia i pliki
pasekpng - plik png używany jako grafika loadingbara/paskaładowania
zdjeciaSlajd - zawarte w nim podzbiory odpowiadają za wyświetlane w programie slajdy.

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

Przykładowy plik konfiguracyjny

{
  "__comment__": "ustawienia debug programów",
      "debug_logslideshow" : "true",
  "__comment__": "poniżej zmienne używane w slideshow",
      "timeForPicture": 5,
      "timeForDownloader": 10, 
      "fullScreenSlideshow": "false",
      "sizeOfLoadingBar": 4,
      "workdirectory": "/home/matball/Projects/czujnikSnapshot",
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

