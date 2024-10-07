import sys

sys.path.append("/BiciMad")
from BiciMad.UrlEMT import UrlEMT
from BiciMad.BiciMad import BiciMad

#test clase BiciMad
bici=BiciMad(2,23)
print(bici.data)
cols=["fleet", "idBike", "station_lock", "station_unlock"]
bici.clean(cols)