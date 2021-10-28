# serializers.py
from rest_framework import serializers

from .models import Historic, PowerPlant


class HistoricSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Historic
        fields = ('load', 'gas_price', 'kerosine_price', 'windturbine_percentage', 'powerplants')


class PowerPlantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PowerPlant
        fields = ('name', 'type', 'efficiency', 'pmin', 'pmax')
