1. Po ściągnieciu repo 

*Kopiowanie zawartości do pliku konfiguracyjnego*
```cp config.json.example config.json```

-plik konfiguracyjny w xml albo json 
  * co ile pobiera zdjecie
  * ??
  * ??
-ogarnac vnc server na ubuntu jako alternatywe do laczenia ssh z klientem
-obecnie zapisywane jest zdjecie i odpalane w oddzielnej przegladarce chcemy by to bylo robione bezposrednio w pythonie zarowno snap jak i wyswietlanie

- najlepiej by screen skladal sie tak jak teraz
  * z zdjecia-snapa

W parametrze np. a - w wysylaniu na adres url='http://czujnikimiejskie.pl/apipost/add/measurement' wysylac wartość jakości sieci/internetu/wifi

uwaga 3004 to numer rasberki w cencnie

=========== pip install Pillow nie PIL - ma jakiś alias w środku

w przypadku błędu przy instalacji
    The headers or library files could not be found for jpeg,
    a required dependency when compiling Pillow from source.

prawdopodobnie brakuje jednej libki w systemie raspbianowi odpowiedzialnej za jpeg

sudo apt-get install libjpeg-dev zlib1g-dev
pip install Pillow
