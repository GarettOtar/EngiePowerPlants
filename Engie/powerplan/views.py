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
        result = powerplan_serilizer.execute(powerplan_data)
        if not result:
            return JsonResponse({'Error': 'not enough power enable'}, status=status.HTTP_412_PRECONDITION_FAILED)
        return JsonResponse(result, status=status.HTTP_200_OK, safe=False)
    return JsonResponse({'Error': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)
