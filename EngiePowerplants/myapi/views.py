#view.py
from .serializers import Powerplan

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(['POST'])
def productionplan(request):
    powerplan_data = JSONParser().parse(request)
    powerplan_serilizer = Powerplan()
    if powerplan_serilizer.is_correct(powerplan_data):
        powerplan_serilizer.execute(powerplan_data)
        return JsonResponse({'foo': 'bar'}, status=status.HTTP_200_OK)
#       return JsonResponse(powerplan_serilizer.execute, status=status.HTTP_200_OK)
    return JsonResponse({'foo': 'bert'}, status=status.HTTP_400_BAD_REQUEST)
#    return JsonResponse(powerplan_serilizer.errors, status=status.HTTP_400_BAD_REQUEST)
