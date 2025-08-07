from datetime import datetime

import pytest

from src.enums.vehicle_orientation import VehicleOrientation
from src.handlers.country_handler import CountryHandler
from src.schemas.vehicle_observation import VehicleObservationRaw


class TestCountryFixHandler:
    @pytest.fixture
    def handler(self):
        return CountryHandler()

    @pytest.mark.parametrize(
        "plate, expected_country_code",
        [
            ("CE123AB", "si"),
            ("go456cd", "si"),
            ("KK-789-EF", "si"),
            ("kp012gh", "si"),
            ("KR_345_IJ", "si"),
            ("lj678kl", "si"),
            ("MB901MN", "si"),
            ("ms234op", "si"),
            ("NM567QR", "si"),
            ("po890st", "si"),
            ("SG123UV", "si"),
            ("XX123YY", None),  # Not a Slovenian municipality code
            ("123AB", None),  # Too short to have a two-letter code
            ("ABCDEF", None),  # Not a valid Slovenian plate pattern
            ("", None),  # Empty plate
            ("  ce  ", "si"),  # Plate with leading/trailing spaces
            (" ce123ab", "si"),  # Plate with leading spaces
            ("ce123ab ", "si"),  # Plate with trailing spaces
        ],
    )
    def test_fix_slovenian_plates(self, handler, plate, expected_country_code):
        observation = VehicleObservationRaw(
            plate=plate,
            plate_score=90,
            country_code=None,
            vehicle_type="car",
            make="Toyota",
            model="Corolla",
            color="red",
            orientation=VehicleOrientation.FRONT,
            timestamp=datetime.now(),
        )

        initial_country_code = observation.country_code
        fixed_observation = handler.fix_slovenian_plates(observation)

        assert fixed_observation.plate == observation.plate

        if expected_country_code:
            assert fixed_observation.country_code == expected_country_code
            assert fixed_observation.country_code != initial_country_code
        else:
            assert fixed_observation.country_code == initial_country_code

    def test_fix_slovenian_plates_no_change_if_already_si(self, handler):
        observation = VehicleObservationRaw(
            plate="CE123AB",
            plate_score=90,
            country_code="si",
            vehicle_type="car",
            make="Toyota",
            model="Corolla",
            color="red",
            orientation=VehicleOrientation.FRONT,
            timestamp=datetime.now(),
        )
        fixed_observation = handler.fix_slovenian_plates(observation)
        assert fixed_observation.country_code == "si"

    def test_fix_slovenian_plates_existing_non_si_country(self, handler):
        observation = VehicleObservationRaw(
            plate="LJ456CD",
            plate_score=90,
            country_code="de",
            vehicle_type="car",
            make="Toyota",
            model="Corolla",
            color="red",
            orientation=VehicleOrientation.FRONT,
            timestamp=datetime.now(),
        )
        fixed_observation = handler.fix_slovenian_plates(observation)
        assert fixed_observation.country_code == "si"
