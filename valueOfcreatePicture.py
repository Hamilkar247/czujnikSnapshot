import argparse
from urllib.request import urlopen

def def_params():
    parser = argparse.ArgumentParser(
            description=
            """
            """
            )
    parser.add_argument("-p", "--plik", default="http://134.122.69.201/config/kiosk/config.json", help="url pliku")
    args = parser.parse_args()
    return args

args=def_params()
URL = args.plik
with urlopen(URL) as f:
    print("Uwaga - czasy są pokazywane w czasie uniwersalnym (greenwich)")
    print(dict(f.getheaders())['Last-Modified'])
    print(dict(f.getheaders()))
