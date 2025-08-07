import json

from src.logger import logger
from src.schemas.vehicle_observation import VehicleObservationRaw


class CountryHandler:
    """Handler for fixing countries with license plate patterns"""

    def __init__(self):
        self.AUSTRIAN_LOOKUP = {}
        self.SLOVENIAN_LOOKUP = {}

        with open("/app/shared-data/municipalities.json", encoding="utf-8") as f:
            data = json.load(f)

            # Process Austria
            if "Austria" in data:
                for state_name, municipalities in data["Austria"].items():
                    for municipality_dict in municipalities:
                        for code, name in municipality_dict.items():
                            self.AUSTRIAN_LOOKUP[code.upper()] = {
                                "country": "at",
                                "state": state_name,
                                "municipality": name,
                            }

            # Process Slovenia
            if "Slovenia" in data:
                municipalities = data["Slovenia"]["Municipalities"]
                for municipality_dict in municipalities:
                    for code, name in municipality_dict.items():
                        self.SLOVENIAN_LOOKUP[code.upper()] = {
                            "country": "si",
                            "state": "Slovenia",
                            "municipality": name,
                        }

    def get_municipality_and_fix_country(
        self, observation: VehicleObservationRaw
    ) -> VehicleObservationRaw:
        """
        Get municipality info and fix country code based on current country detection.

        Args:
            observation: Raw vehicle observation data

        Returns:
            Updated observation with municipality info and potentially fixed country code
        """
        plate_str = observation.plate.strip().upper()

        if len(plate_str) < 1:
            logger.debug(f"Plate '{observation.plate}' too short to be valid")
            return observation

        # Handle Austrian plates
        if observation.country_code == "at":
            return self._check_austrian_municipalities(observation, plate_str)

        # Handle unknown or Slovenian plates
        elif observation.country_code in ["unknown", "si"]:
            return self._check_slovenian_municipalities(observation, plate_str)

        # For other countries
        logger.debug(
            f"No municipality mapping for country '{observation.country_code}'"
        )
        return observation

    def _check_austrian_municipalities(
        self, observation: VehicleObservationRaw, plate_str: str
    ) -> VehicleObservationRaw:
        """Check Austrian municipality codes"""

        # Try 2-letter codes first
        if len(plate_str) >= 2:
            code_2 = plate_str[:2]
            if code_2 in self.AUSTRIAN_LOOKUP:
                municipality_info = self.AUSTRIAN_LOOKUP[code_2]
                observation.municipality = code_2
                logger.debug(
                    f"Austrian plate mapped to region: "
                    f"{municipality_info['municipality']}, {municipality_info['state']} (code: {code_2})"
                )
                return observation

        # Try 1-letter codes
        code_1 = plate_str[:1]
        if code_1 in self.AUSTRIAN_LOOKUP:
            municipality_info = self.AUSTRIAN_LOOKUP[code_1]
            observation.municipality = code_1
            logger.debug(
                f"Austrian plate mapped to region: "
                f"{municipality_info['municipality']}, {municipality_info['state']} (code: {code_1})"
            )
            return observation

        logger.debug(f"No Austrian region match found for plate '{observation.plate}'")
        return observation

    def _check_slovenian_municipalities(
        self, observation: VehicleObservationRaw, plate_str: str
    ) -> VehicleObservationRaw:
        """Check Slovenian municipality codes and fix country if unknown"""

        # Try 2-letter codes
        if len(plate_str) >= 2:
            code_2 = plate_str[:2]
            if code_2 in self.SLOVENIAN_LOOKUP:
                municipality_info = self.SLOVENIAN_LOOKUP[code_2]
                observation.municipality = code_2

                # Fix country code if it was unknown
                if observation.country_code == "unknown":
                    observation.country_code = "si"
                    logger.debug(
                        f"Fixed plate country changed to 'si' "
                        f"(region: {municipality_info['municipality']}, code: {code_2})"
                    )
                else:
                    logger.debug(
                        f"Slovenian plate mapped to region: "
                        f"{municipality_info['municipality']} (code: {code_2})"
                    )

                return observation

        logger.debug("No Slovenian region match found for plate")
        return observation
