# LLM_API/urls.py
from django.urls import path
from .views import GenerateView, SaveItineraryView, GetItineraryView, CompleteItineraryView

urlpatterns = [
    path('generate/', GenerateView.as_view(), name='LLM-generate'),
    path('save-itinerary/', SaveItineraryView.as_view(), name='LLM-save-itinerary'),
    path('complete-itinerary/', CompleteItineraryView.as_view(), name='LLM-complete-itinerary'),
    path('itinerary/<int:itinerary_id>/', GetItineraryView.as_view(), name='LLM-get-itinerary'),
]