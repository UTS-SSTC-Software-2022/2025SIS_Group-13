from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Itinerary, DailySchedule, POI
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password cannot be left blank.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create(
            username=username,
            password=make_password(password)
        )
        return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def homepage(request):
    user = request.user
    itineraries = Itinerary.objects.filter(user=user)

    data = []
    for itinerary in itineraries:
        schedules = DailySchedule.objects.filter(itinerary=itinerary)
        schedule_data = []
        for s in schedules:
            pois = POI.objects.filter(schedules=s)
            schedule_data.append({
                "day": s.day_number,
                "summary": s.summary,
                "pois": [p.name for p in pois]
            })
        data.append({
            "title": itinerary.title,
            "days": schedules.count(),
            "schedules": schedule_data
        })

    return Response({
        "user": user.username,
        "itineraries": data
    })
