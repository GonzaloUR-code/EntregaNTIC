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
from BiciMad.UrlEMT import UrlEMT

class BiciMad:
    """

    """

    def __init__(self, month:int, year:int):
        """
          Inicializa un objeto BiciMad con los datos correspondientes al mes y año proporcionados.

          Parámetros
          ----------
          month : int
              El mes (en formato numérico) para el cual se obtendrán los datos.
          year : int
              El año para el cual se obtendrán los datos.

          Al construir el objeto, se obtienen automáticamente los datos de uso llamando al método estático get_data.
          """
        self.__month = month
        self.__year=year
        self.__data=BiciMad.get_data(self.__month, self.__year)

    @staticmethod
    def get_data(month:int, year:int) -> pd.DataFrame:
        """
         Obtiene los datos de uso de BiciMad para el mes y año proporcionados.

         Este método accede a la URL correspondiente para descargar los datos en formato CSV
         y los transforma en un DataFrame de pandas. Las fechas se convierten en tipo `datetime`
         y el índice del DataFrame es la fecha en que tuvo lugar el viaje.

         Parámetros
         ----------
         month : int
             El mes (en formato numérico) para el cual se quieren obtener los datos.
         year : int
             El año para el cual se quieren obtener los datos.

         Return
         -------
         pd.DataFrame

         """
        urls_valida = UrlEMT()
        csvfile = urls_valida.get_csv(month, year)
        df = pd.read_csv(csvfile, sep=';',
                         usecols=['fecha','idBike', 'fleet', 'trip_minutes', 'geolocation_unlock', 'address_unlock', 'unlock_date', 'locktype', 'unlocktype',
                          'geolocation_lock', 'address_lock', 'lock_date', 'station_unlock',
                        'unlock_station_name', 'station_lock', 'lock_station_name'], index_col='fecha',
                         parse_dates=['fecha', 'unlock_date', 'lock_date'])
        return df

    @property
    def data(self):
        return self.__data

    def __str__(self):
        return str(self.__data)

    def clean(self,cols:list) -> None:
        """
          Limpia los datos de uso de BiciMad eliminando filas vacías y asegurando que los valores
          de las columnas especificadas sean de tipo cadena.

          Parámetros
          ----------
          cols: list
              Lista de nombres de columnas que deben ser convertidas a tipo `str`.

          Return
          -------
          None
          """
        self.__data.dropna(how='all', axis=0, inplace=True)
        for col in cols:
            if col in self.__data.columns:
                self.__data[col] = self.__data[col].map(lambda x: str(x))

