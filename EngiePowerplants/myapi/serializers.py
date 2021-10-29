# serializers.py
from rest_framework import serializers
import logging

from .constants import FuelType, FUEL_TYPE, PowerplantType, POWERPLANT_TYPE, POWERPLANT_ELEM

logger = logging.getLogger(__name__)


class Powerplan(serializers.Serializer):

    def rec_powerplant_aggregator(self, data, loadout, loadPrepared):
        selected_powerplant = None
        power_generated = 0
        for powerplant in data["powerplants"]:
            if selected_powerplant is None:
                selected_powerplant = powerplant
                continue
            if powerplant["type"] == PowerplantType.WINDTURBINE.value:
                selected_powerplant = powerplant
                power_generated = selected_powerplant["pmax"]
                if loadPrepared + power_generated > data['load']:
                    power_generated = data['load'] - loadPrepared
                break


        loadout.append({"name": selected_powerplant["name"], "p": power_generated})
        data["powerplants"].pop(data["powerplants"].index(selected_powerplant))
        if loadPrepared == data['load']:
            return loadout
        if not data["powerplants"]:
            return False
        return self.rec_powerplant_aggregator(data, loadout, loadPrepared)

    def new_powerplant_detailed(self, fuels, powerplants):
        powerplant_detailed = []
        for powerplant in powerplants:
            if powerplant["efficiency"] <= 0:
                continue
            if powerplant["type"] is PowerplantType.WINDTURBINE.value and fuels[FuelType.WIND.value] <= 0:
                continue
            newPowerplant = powerplant
            if powerplant["type"] is PowerplantType.WINDTURBINE.value:
                newPowerplant["pmax"] = int(powerplant["efficiency"] * powerplant["pmax"] *
                                            (fuels[FuelType.WIND.value] / 100))
            else:
                newPowerplant["pmin_load_value"] = int(powerplant["pmin"] * powerplant["efficiency"])
                newPowerplant["pmax_load_value"] = int(powerplant["pmax"] * powerplant["efficiency"])
            if powerplant["type"] is PowerplantType.WINDTURBINE.value:
                powerplant_detailed.insert(0, newPowerplant)
            else:
                powerplant_detailed.append(newPowerplant)
        return powerplant_detailed

    def execute(self, data):
        data["powerplants"] = self.new_powerplant_detailed(data["fuels"], data["powerplants"])
        result = self.rec_powerplant_aggregator(data, [], 0)
        if not result:
            return False
        return result

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
