# serializers.py
from rest_framework import serializers
from itertools  import combinations

import logging

from .constants import FuelType, FUEL_TYPE, PowerplantType, POWERPLANT_TYPE, POWERPLANT_ELEM

logger = logging.getLogger(__name__)


class Powerplan(serializers.Serializer):

    def match_fuel_cost(self, fuels, powerplant_type):
        if powerplant_type == PowerplantType.GASFIRED.value:
            return fuels[FuelType.GAS.value]
        if powerplant_type == PowerplantType.TURBOJET.value:
            return fuels[FuelType.KEROSINE.value]
        return False

    def price_powerplant_possibility(self, powerplant_set, fuels, load):
        final_price = 0
        charged_load = 0
        result = []
        for powerplant in powerplant_set:
            charged_load += powerplant["pmin_load_value"]
            final_price += 0 if powerplant["type"] == PowerplantType.WINDTURBINE.value else \
                powerplant["pmin_load_value"] * self.match_fuel_cost(fuels, powerplant["type"])
            result.append({"name": powerplant["name"], "p": powerplant["pmin_load_value"]})
            if charged_load > load:
                return powerplant_set, final_price, False
        wind_powerplants = sorted((powerplant for powerplant in powerplant_set if powerplant["type"] ==
                            PowerplantType.WINDTURBINE.value), key=lambda d: d["pmax"])
        for wind_powerplant in wind_powerplants:
            if (load - charged_load) == 0:
                continue
            load_gap = wind_powerplant["pmax_load_value"] - wind_powerplant["pmin_load_value"]
            toLoad = load_gap if (load - charged_load) > load_gap else (load - charged_load)
            charged_load += toLoad
            for elem in result:
                if elem["name"] == wind_powerplant["name"]:
                    result[result.index(elem)]["p"] += toLoad
        other_powerplants = sorted((powerplant for powerplant in powerplant_set if powerplant["type"] !=
                             PowerplantType.WINDTURBINE.value), key=lambda d: d["efficiency"], reverse=True)
        for other_powerplant in other_powerplants:
            if (load - charged_load) == 0:
                continue
            load_gap = other_powerplant["pmax_load_value"] - other_powerplant["pmin_load_value"]
            toLoad = load_gap if (load - charged_load) > load_gap else (load - charged_load)
            charged_load += toLoad
            final_price += load_gap * self.match_fuel_cost(fuels, other_powerplant["type"])
            for elem in result:
                if elem["name"] == other_powerplant["name"]:
                    result[result.index(elem)]["p"] += toLoad
        if load != charged_load:
            return result, final_price, False
        return result, final_price, True

    def new_powerplant_detailed(self, fuels, powerplants):
        powerplant_detailed = []
        for powerplant in powerplants:
            if powerplant["efficiency"] <= 0 or powerplant["pmax"] <= 0 or powerplant["pmax"] < powerplant["pmin"]:
                continue
            if powerplant["type"] == PowerplantType.WINDTURBINE.value and fuels[FuelType.WIND.value] <= 0:
                continue
            newPowerplant = powerplant
            if powerplant["type"] == PowerplantType.WINDTURBINE.value:
                newPowerplant["pmin_load_value"] = 0 if powerplant["pmin"] == 0 else \
                    int(powerplant["efficiency"] * powerplant["pmin"] * (fuels[FuelType.WIND.value] / 100))
                newPowerplant["pmax_load_value"] = int(powerplant["efficiency"] * powerplant["pmax"] *
                                            (fuels[FuelType.WIND.value] / 100))
            else:
                newPowerplant["pmin_load_value"] = 0 if powerplant["pmin"] == 0 else \
                    int(powerplant["pmin"] * powerplant["efficiency"])
                newPowerplant["pmax_load_value"] = int(powerplant["pmax"] * powerplant["efficiency"])
            if powerplant["type"] == PowerplantType.WINDTURBINE.value:
                powerplant_detailed.insert(0, newPowerplant)
            else:
                powerplant_detailed.append(newPowerplant)
        return powerplant_detailed

    def execute(self, data):
        data["powerplants"] = self.new_powerplant_detailed(data["fuels"], data["powerplants"])
        listed_powerplants = []
        for n in range(0, len(data["powerplants"]) + 1):
            listed_powerplants.append([i for i in combinations(data["powerplants"], n)])
        priced_powerplant_list = []
        for possibilities in listed_powerplants:
            for possibility in possibilities:
                priced_powerplant_list.append(self.price_powerplant_possibility(possibility, data["fuels"],
                                                                                data["load"]))
        result = sorted((powerplant for powerplant in priced_powerplant_list if powerplant[2] is True),
                        key=lambda d: d[1]).pop(0)
        if not result[2]:
            return False
        for missing_powerplant in data["powerplants"]:
            if not any(d["name"] == missing_powerplant["name"] for d in result[0]):
                result[0].append({"name": missing_powerplant["name"], "p": 0})
        logger.warning(result[0])
        return result[0]

    def check_fuel(self, fuels):
        if not all(elem in fuels for elem in FUEL_TYPE):
            return False
        if len(fuels) != len(FUEL_TYPE):
            return False
        for fuel in fuels:
            try:
                float(fuels[fuel])
            except ValueError:
                return False
        return True

    def check_powerplant_type(self, powerplant):
        if powerplant["type"] not in POWERPLANT_TYPE:
            return False
        try:
            float(powerplant["efficiency"])
            int(powerplant["pmin"])
            int(powerplant["pmax"])
        except ValueError:
            return False
        return True

    def check_powerplants(self, powerplants):
        for powerplant in powerplants:
            if not all(elem in powerplant for elem in POWERPLANT_ELEM):
                return False
            if len(powerplant) != len(POWERPLANT_ELEM):
                return False
            self.check_powerplant_type(powerplant)
        return True

    def is_correct(self, data):
        if not all(elem in data for elem in ("load", "fuels", "powerplants")):
            return False
        try:
            int(data['load'])
        except ValueError:
            pass
        if not self.check_fuel(data['fuels']):
            return False
        if not self.check_powerplants(data['powerplants']):
            return False
        return True
