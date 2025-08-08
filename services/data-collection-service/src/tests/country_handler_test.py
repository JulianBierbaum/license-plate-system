from datetime import datetime

import pytest

from src.enums.vehicle_orientation import VehicleOrientation
from src.handlers.country_handler import CountryHandler
from src.schemas.vehicle_observation import VehicleObservationRaw


@pytest.fixture
def handler():
    """Create a CountryHandler with minimal test data for Austria and Slovenia."""
    data = {
        'Austria': {
            'Burgenland': [
                {'E': 'Eisenstadt-Stadt'},
                {'EU': 'Eisenstadt/Umgebung'},
            ],
            'Kärnten': [
                {'K': 'Klagenfurt-Stadt'},
                {'KL': 'Klagenfurt/Land'},
            ],
        },
        'Slovenia': {
            'Municipalities': [
                {'CE': 'Celje'},
                {'LJ': 'Ljubljana'},
            ]
        },
    }
    return CountryHandler(data=data)


def make_observation(plate: str, country_code: str | None):
    """Helper to create a VehicleObservationRaw for tests."""
    return VehicleObservationRaw(
        plate=plate,
        plate_score=90,
        country_code=country_code,
        vehicle_type='car',
        make='Toyota',
        model='Corolla',
        color='red',
        orientation=VehicleOrientation.FRONT,
        timestamp=datetime.now(),
    )


class TestCountryHandler:
    @pytest.mark.parametrize(
        'plate, initial_country, expected_country, expected_municipality',
        [
            ('CE123AB', 'unknown', 'si', 'CE'),
            ('lj999xx', 'unknown', 'si', 'LJ'),
            ('CE123AB', 'si', 'si', 'CE'),
            ('LJ456CD', 'de', 'de', None),
            ('XX123YY', 'unknown', 'unknown', None),
        ],
    )
    def test_slovenian_lookup(
        self,
        handler,
        plate,
        initial_country,
        expected_country,
        expected_municipality,
    ):
        obs = make_observation(plate, initial_country)
        fixed = handler.get_municipality_and_fix_country(obs)
        assert fixed.country_code == expected_country
        assert fixed.municipality == expected_municipality

    @pytest.mark.parametrize(
        'plate, initial_country, expected_country, expected_municipality',
        [
            ('E123AB', 'at', 'at', 'E'),
            ('EU456CD', 'at', 'at', 'EU'),
            ('E123AB', 'de', 'de', None),
            ('ZZ999ZZ', 'at', 'at', None),
        ],
    )
    def test_austrian_lookup(
        self,
        handler,
        plate,
        initial_country,
        expected_country,
        expected_municipality,
    ):
        obs = make_observation(plate, initial_country)
        fixed = handler.get_municipality_and_fix_country(obs)
        assert fixed.country_code == expected_country
        assert fixed.municipality == expected_municipality
