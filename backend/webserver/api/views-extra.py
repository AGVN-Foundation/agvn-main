from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from helper import *
from .models.Occupation import Occupation


@api_view(['POST'])
def post_offers(request):
    data = request.data
    token = data['token']
    voter = get_voter(token)

    if not voter:
        return Response(data={"error": "Invalid Voter"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # collect new occupation and level
        new_occ = data['job_offer']['occupation']
        new_level = data['job_offer']['level']

        # find the occupation
        Occupation.objects.filter(type=new_occ)

        voter.current_occupation = new_occ
        voter.occupation_rank = new_level

    except Exception as e:
        return Response(data={"error": "Body is not in the right format"}, status=status.HTTP_400_BAD_REQUEST)
