import sys

sys.path.append("/BiciMad")
from BiciMad.UrlEMT import UrlEMT
from BiciMad.BiciMad import BiciMad

# test de la clase urlEMT
urls_valida=UrlEMT()
print(urls_valida)
csvfile =urls_valida.get_csv(month=10,year=21)

print(csvfile.getvalue())
