from src.logger import logger
from src.schemas.vehicle_observation import VehicleObservationRaw


class CountryFixHandler:
    """Handler for fixing countries with license plate patterns"""

    def fix_slovenian_plates(
        self, observation: VehicleObservationRaw
    ) -> VehicleObservationRaw:
        """fix for slovenian plates
            (currently always returning as unknown country)

        Args:
            observation (VehicleObservationRaw): raw return data from the plate analyzer

        Returns:
            VehicleObservationRaw: raw data with fixed country when a match was found
        """
        _municipality_list = (
            "ce",
            "go",
            "kk",
            "kp",
            "kr",
            "lj",
            "mb",
            "ms",
            "nm",
            "po",
            "sg",
        )  # source: https://en.wikipedia.org/wiki/Vehicle_registration_plates_of_Slovenia

        plate_str = observation.plate.strip().lower()

        if len(plate_str) >= 2:
            plate_code = plate_str[:2]

            if plate_code in _municipality_list:
                observation.country_code = "si"

                logger.info(
                    f"Fixed plate '{observation.plate}': "
                    f"country changed to {observation.country_code}"
                )
                return observation

        logger.info(f"No Slovenian region fix applied for plate {observation.plate}")
        return observation
