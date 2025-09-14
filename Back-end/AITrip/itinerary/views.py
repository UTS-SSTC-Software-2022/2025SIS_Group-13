from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Itinerary, DailySchedule, POI
from .serializers import ItinerarySerializer, DailyScheduleSerializer, POISerializer
from django_filters.rest_framework import DjangoFilterBackend

from utils.response import CustomModelViewSet

class ItineraryViewSet(CustomModelViewSet):
    queryset = Itinerary.objects.all()
    serializer_class = ItinerarySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class DailyScheduleViewSet(CustomModelViewSet):
    queryset = DailySchedule.objects.all()
    serializer_class = DailyScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

class POIViewSet(CustomModelViewSet):
    queryset = POI.objects.all()
    serializer_class = POISerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'