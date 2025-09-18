from django.db import models
from django.conf import settings
from itinerary.models import Itinerary, POI, DailySchedule

class Review(models.Model):
    CATEGORY_CHOICES = [
        ('itinerary', 'Itinerary'),
        ('poi', 'POI'),
        ('daily_schedule', 'Daily Schedule'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, null=True, blank=True)
    poi = models.ForeignKey(POI, on_delete=models.CASCADE, null=True, blank=True)
    feedback_text = models.TextField()
    
    def __str__(self):
        return f"{self.user} - {self.category}"
