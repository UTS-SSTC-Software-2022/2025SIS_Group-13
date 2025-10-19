from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItineraryViewSet, DailyScheduleViewSet, POIViewSet, MemoirViewSet

router = DefaultRouter()
router.register(r'itineraries', ItineraryViewSet, basename='itinerary')
router.register(r'daily-schedules', DailyScheduleViewSet, basename='daily-schedule')
router.register(r'pois', POIViewSet, basename='poi')
router.register(r'memoir', MemoirViewSet, basename='memoir')

urlpatterns = [
    path('', include(router.urls))
]