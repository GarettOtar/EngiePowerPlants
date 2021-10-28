from rest_framework import viewsets
from .serializers import HistoricSerializer
from .models import Historic, PowerPlant


class HistoricViewSet(viewsets.ModelViewSet):
    queryset = Historic.objects.all()
    serializer_class = HistoricSerializer
