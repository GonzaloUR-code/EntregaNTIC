import sys

sys.path.append("/BiciMad")
from B import UrlEMT
urls_valida=UrlEMT()
print(urls_valida)
csvfile =urls_valida.get_csv(month=10,year=21)

print(csvfile.getvalue())
