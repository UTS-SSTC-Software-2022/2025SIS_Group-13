from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItineraryViewSet, DailyScheduleViewSet, POIViewSet, test_itinerary_list

router = DefaultRouter()
router.register(r'itineraries', ItineraryViewSet, basename='itinerary')
router.register(r'daily-schedules', DailyScheduleViewSet, basename='daily-schedule')
router.register(r'pois', POIViewSet, basename='poi')

urlpatterns = [
    path('test-itineraries/', test_itinerary_list, name='test-itinerary-list'),
    path('', include(router.urls))
]