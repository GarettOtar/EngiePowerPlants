from django.db import models
from .constants import POWERPLANT_TYPE


class PowerPlant(models.Model):
    name = models.TextField
    type = models.TextField(POWERPLANT_TYPE)
    efficiency = models.FloatField()
    pmin = models.IntegerField()
    pmax = models.IntegerField()


class Historic(models.Model):
    call = models.CharField(max_length=11)
    call_date = models.DateTimeField()
    load = models.IntegerField()
    gas_price = models.FloatField()
    kerosine_price = models.FloatField()
    windturbine_percentage = models.FloatField()
    powerplants = models.ForeignKey(PowerPlant, on_delete=models.CASCADE)

    def __str__(self):
        return self.call

    class Meta:
        ordering = ['call']
