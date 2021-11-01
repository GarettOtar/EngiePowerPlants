from enum import Enum


POWERPLANT_TYPE = ["gasfired", "turbojet", "windturbine"]


class PowerplantType(Enum):
    GASFIRED = "gasfired"
    TURBOJET = "turbojet"
    WINDTURBINE = "windturbine"


FUEL_TYPE = ["gas(euro/MWh)", "kerosine(euro/MWh)", "co2(euro/ton)", "wind(%)"]


class FuelType(Enum):
    GAS = "gas(euro/MWh)"
    KEROSINE = "kerosine(euro/MWh)"
    CO2 = "co2(euro/ton)"
    WIND = "wind(%)"


POWERPLANT_ELEM = [
    "name",
    "type",
    "efficiency",
    "pmin",
    "pmax",
]
