# serializers.py
from rest_framework import serializers
import logging

from .constants import FUEL_TYPE, POWERPLANT_TYPE, POWERPLANT_ELEM

logger = logging.getLogger(__name__)


class Powerplan(serializers.Serializer):

    def addNewpowerplant(self, data, loadout, loadPrepared):
        if loadout is None:
            loadout = []
        for 
        return data, loadout, loadPrepared

    def execute(self, data, loadout=None, loadPrepared=0):
        data, loadout, loadPrepared = self.addNewpowerplant(data, loadout, loadPrepared)
        if loadPrepared == data['load']:
            return {'result': True}
        return self.execute(data, loadout, loadPrepared)

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
