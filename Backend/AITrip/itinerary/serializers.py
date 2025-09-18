from rest_framework import serializers
from .models import Itinerary, DailySchedule, POI

class POISerializer(serializers.ModelSerializer):
    class Meta:
        model = POI
        fields = '__all__'
        read_only_fields = ('poi_id', 'create_time', 'update_time')

class DailyScheduleSerializer(serializers.ModelSerializer):
    pois = POISerializer(many=True, read_only=True)  
    class Meta:
        model = DailySchedule
        fields = '__all__'
        read_only_fields = ('schedule_id', 'create_time', 'update_time')

class ItinerarySerializer(serializers.ModelSerializer):
    daily_schedules = DailyScheduleSerializer(many=True, read_only=True) 

    class Meta:
        model = Itinerary
        fields = '__all__'
        read_only_fields = ('itinerary_id', 'create_time', 'update_time')