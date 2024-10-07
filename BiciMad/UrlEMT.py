import pandas as pd
import numpy as np
import zipfile, io
import requests
import csv
from typing import TextIO
from typing import TypeVar
import re
from pandas import Series

import matplotlib.pyplot as plt


class UrlEMT:
    """
    clase que permita recopilar todos los enlaces que hay en la web de la EMT
    (https://opendata.emtmadrid.es/Datos-estaticos/Datos-generales-(1)), que se
    corresponden con datos de uso de bicicletas desde Junio de 2021. Los enlaces que cumplen
    esta restricción son los que denominaremos a partir de ahora enlaces válidos.

    Estos enlaces contienen la cadena trips_YY_MM_monthName.csv donde
     YY representa el año, MM representa el mes y monthName representa el nombre del mes en inglés.

    """
    EMT = 'https://opendata.emtmadrid.es/'
    GENERAL = "/Datos-estaticos/Datos-generales-(1)"

    def __init__(self):
        """
        Parametros
        ----------
        url: string que representa la direccioón web de la EMT
        """
        self.url = UrlEMT.EMT+UrlEMT.GENERAL
        self.__enlaces_validos=UrlEMT.select_valid_urls (self.url)

    @staticmethod
    def get_links(html: str) -> list:
        """
        :param html: Una cadena que contiene el contenido HTML desde el cual se necesitan extraer las URLs.
        :return: Una lista de URLs extraídas del contenido HTML proporcionado.
        """

        # patron = r'href=["\'](https?://[^\s"\'<>]+)["\']'
        patron = r'href=["\']?([^"\'>]+)["\']?'

        links = re.findall(patron, html)
        return links

    @staticmethod
    def select_valid_urls (url: str) -> TextIO:
        """

        Selecciona las URLs válidas de la página web proporcionada.
        :param url: La url de la EMT.
        :return: Una lista de URLs válidas.

        """
        try:
            html = requests.get(url)
            if html.status_code != 200:
                raise ConnectionError(f"Fallo en el acceso al servidor de la EMT {url}, status code: {html.status_code}")
            # convertimos de bytes a texto html
            with open("codigo_html_emt", "wb") as file:
                file.write(html.content)
            html = html.content.decode('utf-8')
            url_valid=UrlEMT.get_links(html)
            return url_valid
        except requests.RequestException as fe:
            raise ConnectionError(f"Error de conexión a  {url}: {str(fe)}")

    def get_url(self,month:int, year:int)->str:
        """
       Obtiene la URL del archivo CSV para un mes y año dados.
       :param month: Mes (int).
       :param year: Año (int).
       :return: La URL del archivo CSV.
       :raise: ValueError si el mes o año no son válidos, o si no se encuentra la URL.
       """
        month_str = f"{month:02d}"
        year_str = f"{year:02d}"

        #comprobamos que los arg de entrada son validos en formato
        patron_mes = r'^(0[1-9]|1[0-2])$'
        patron_year=r'^2[1-3]$'

        error=[]
        if not re.findall(patron_mes, month_str):
            error.append(f"El formato del parámetro de entrada {month} no es valido. El formato debe ser MM en formato integer.")
        if not re.findall(patron_year, year_str):
            error.append(f"El formato del parámetro de entrada {year} no es valido. El formato debe ser YY con años entre 21 y 23.")
        if error:
            raise ValueError(" ".join(error))

        patron="trips_"+year_str+"_"+month_str
        url_encontrado=[]
        for url in self.__enlaces_validos:
            if patron in url:
                url_encontrado=url
                return url_encontrado
        if not url_encontrado:
            raise ValueError(f'No existen una url para los meses {month} y {year} en el web de la EMT')


    def csv_from_zip(self, url: str) -> TextIO:
        """
        Descarga un archivo ZIP desde la URL proporcionada, extrae un archivo CSV específico y devuelve su contenido como un objeto TextIO.

        :input
        url (string): La URL del archivo ZIP a descargar.

        :Output
        TextIO: Un flujo de texto en memoria del contenido del archivo CSV extraído.

        :raise:
        ConnectionError: Si hay un error durante el proceso de descarga o si el código de estado de la respuesta no es 200.
        requests.RequestException: Si hay un error durante la operación de la solicitud.
        """
        try:
            zfile = requests.get(url)
            if zfile.status_code != 200:
                raise ConnectionError(f"Fallo en la descarga del fihero ZIP {url}, status code: {zfile.status_code}")
            # convertimos los datos de bytes del zip en un  objeto archivo que nos permite leer a psoteiro
            bytes = io.BytesIO(zfile.content)
            zfile = zipfile.ZipFile(bytes)

            # Buscamos el archivo CSV dentro del ZIP
            fileCSV = None
            for tipo in zfile.namelist():
                if tipo.endswith('.csv'):
                    fileCSV = tipo
                    break

            if fileCSV is None:
                raise FileNotFoundError("No hay archivo CSV en el zip")

            with zfile.open(fileCSV) as f:
                contents = f.read()
                # decodificamos de bytes a cadenas de carcatertes
                contentstr = contents.decode('utf-8')
                # convertimos en objeto archivo para su manipulacion y lo guardamos temporalmente en memoria
                fstr = io.StringIO(contentstr)

                '''        
                # Extraemos el contenido del archivo CSV y lo convertimos en un objeto de tipo TextIO
                csv_file = zip_file.open(csv_filename)
                csv_text = io.TextIOWrapper(csv_file, encoding='utf-8')

                OTRA OPCION?
                csvfile = csv_from_zip(url=path_url)
                usos = get_data(csvfile)
                '''
            return fstr

        except requests.RequestException as fe:
            raise ConnectionError(f"Error de conexión a  {url}: {str(fe)}")


    def get_csv(self, month: int, year: int) -> TextIO:
        """
        Obtiene el contenido del archivo CSV para un mes y año dados.
        :param month: Mes (int).
        :param year: Año (int).
        :return: Un flujo de texto en memoria del contenido del archivo CSV.
        """
        getURL = self.get_url(month, year)
        getURL=UrlEMT.EMT[:-1]+getURL
        csv_file = self.csv_from_zip(getURL)

        return csv_file
