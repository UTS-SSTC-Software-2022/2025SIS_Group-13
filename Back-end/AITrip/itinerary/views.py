from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Itinerary, DailySchedule, POI
from .serializers import ItinerarySerializer, DailyScheduleSerializer, POISerializer

class ItineraryViewSet(viewsets.ModelViewSet):
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DailyScheduleViewSet(viewsets.ModelViewSet):
    queryset = DailySchedule.objects.all()
    serializer_class = DailyScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

class POIViewSet(viewsets.ModelViewSet):
    queryset = POI.objects.all()
    serializer_class = POISerializer
    permission_classes = [permissions.IsAuthenticated]