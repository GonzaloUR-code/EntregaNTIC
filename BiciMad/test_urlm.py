import sys

sys.path.append("C:/Users/gutrilla/PycharmProjects/Entregable_python/BiciMad")
from UrlEMT import UrlEMT
urls_valida=UrlEMT()
print(urls_valida)
csvfile =urls_valida.get_csv(month=10,year=21)

print(csvfile.getvalue())