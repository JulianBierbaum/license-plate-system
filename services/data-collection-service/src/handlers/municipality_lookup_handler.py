import json

from src.config import settings


class MunicipalityHandler:
    _municipality_lookup: dict[str, tuple[str, str]] = {}
    _is_initialized: bool = False

    def __init__(self):
        if not self._is_initialized:
            self._initialize()

    def _initialize(self):
        if not self._municipality_lookup:
            try:
                with open(settings.municipalities_json_file, encoding="utf-8") as f:
                    data = json.load(f)
                    for state, municipalities in data.items():
                        for municipality_dict in municipalities:
                            for code, name in municipality_dict.items():
                                self._municipality_lookup[code.upper()] = (state, name)
                self._is_initialized = True
            except FileNotFoundError:
                print(
                    f"Error: Municipality data file not found at {settings.municipalities_json_file}"
                )
                self._is_initialized = False
            except json.JSONDecodeError:
                print(
                    f"Error: Could not decode JSON from {settings.municipalities_json_file}"
                )
                self._is_initialized = False
            except Exception as e:
                print(f"An unexpected error occurred during initialization: {e}")
                self._is_initialized = False

    def get_municipality_info(self, plate_str: str) -> tuple[str, str]:
        if not self._is_initialized:
            print("Warning: MunicipalityHandler not initialized. Returning empty info.")
            return "", ""

        if not plate_str:
            return "", ""

        # Check for 2-letter region codes first
        if len(plate_str) >= 2:
            code_2 = plate_str[:2].upper()
            if code_2 in self._municipality_lookup:
                return self._municipality_lookup[code_2]

        # Then try 1-letter codes
        if len(plate_str) >= 1:
            code_1 = plate_str[:1].upper()
            if code_1 in self._municipality_lookup:
                return self._municipality_lookup[code_1]

        return "", ""
