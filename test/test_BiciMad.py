import pytest
from BiciMad.BiciMad import BiciMad


class TestBiciMad:

    @pytest.fixture(autouse=True)
    def setUp(self):
        self.bici = BiciMad()

        # Configuramos los enlaces válidos
        self.urlemt._UrlEMT__enlaces_validos = [
            "http://example.com/trips_21_01",
            "http://example.com/trips_22_06",
            "http://example.com/trips_23_12",
        ]

    @pytest.mark.parametrize("month, year, expected_url", [
        (1, 21, "http://example.com/2023/01"),
        (6, 22, "http://example.com/2024/06"),
        (12, 23, "http://example.com/2025/12"),
    ])
    def test_get_url_with_valid_parameters(self, month, year, expected_url):
        assert self.urlemt.get_url(month, year) == expected_url

    @pytest.mark.parametrize("invalid_month, year", [
        (0, 2023),
        (-5, 2023),
        (13, 2023),
        (15, 2023),
    ])
    def test_get_url_with_invalid_month(self, invalid_month, year):
        with pytest.raises(ValueError, match="Mes no válido"):
            self.urlemt.get_url(invalid_month, year)

    @pytest.mark.parametrize("month, invalid_year", [
        (5, 1800),
        (5, 1500),
        (5, -1),
    ])
    def test_get_url_with_invalid_year(self, month, invalid_year):
        with pytest.raises(ValueError, match="Año no válido"):
            self.urlemt.get_url(month, invalid_year)

    @pytest.mark.parametrize("invalid_month, invalid_year", [
        (0, 1800),
        (13, 1800),
        (-5, 1500),
        (15, -1),
    ])
    def test_get_url_with_invalid_month_and_year(self, invalid_month, invalid_year):
        with pytest.raises(ValueError):
            self.urlemt.get_url(invalid_month, invalid_year)

    @pytest.mark.parametrize("month, year", [
        (1, 3000),
        (6, 3001),
        (12, 3002),
    ])
    def test_get_url_with_valid_parameters_but_not_in_links(self, month, year):
        with pytest.raises(ValueError, match="El enlace no está en la lista de enlaces válidos"):
            self.urlemt.get_url(month, year)

# Para ejecutar las pruebas, usa el siguiente comando en la línea de comandos:
# pytest nombre_del_archivo.py

