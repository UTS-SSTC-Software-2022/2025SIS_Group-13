# users/models.py

from django.db import models
from django.contrib.auth.models import User


class Itinerary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

class DailySchedule(models.Model):
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE)
    day_number = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    summary = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

class POI(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    target_audience = models.CharField(max_length=255, null=True, blank=True)
    booking_link = models.URLField(max_length=500, null=True, blank=True)
    avg_duration = models.IntegerField(null=True, blank=True)
    opening_hours = models.CharField(max_length=255, null=True, blank=True)
    ticket_price = models.CharField(max_length=100, null=True, blank=True)
    review_summary = models.TextField(null=True, blank=True)
    review_source = models.CharField(max_length=255, null=True, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    schedules = models.ManyToManyField(DailySchedule, through='SchedulePOI')

class SchedulePOI(models.Model):
    schedule = models.ForeignKey(DailySchedule, on_delete=models.CASCADE)
    poi = models.ForeignKey(POI, on_delete=models.CASCADE)

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE)
    schedule = models.ForeignKey(DailySchedule, on_delete=models.CASCADE)
    feedback_text = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
