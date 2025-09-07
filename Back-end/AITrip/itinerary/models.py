from django.db import models
from django.conf import settings

# Create your models here.
class Itinerary(models.Model):
    itinerary_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='itineraries',
        verbose_name='User',
        db_index=True,
        help_text='Owner of the itinerary'
    )
    title = models.CharField(
        max_length=255,
        verbose_name='Title'
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Create Time',
        db_index=True
    )
    update_time = models.DateTimeField(
        auto_now=True,
        verbose_name='Update Time',
        db_index=True
    )

    class Meta:
        db_table = 'itineraries'
        verbose_name = 'Itinerary'
        verbose_name_plural = 'Itineraries'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['create_time']),
            models.Index(fields=['update_time']),
        ]

    def __str__(self):
        return f"{self.title} ({self.user})"


class DailySchedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    itinerary = models.ForeignKey(
        Itinerary,
        on_delete=models.CASCADE,
        related_name='daily_schedules',
        verbose_name='Itinerary',
        db_index=True
    )
    day_number = models.IntegerField(
        verbose_name='Day Number'
    )
    start_time = models.TimeField(
        verbose_name='Start Time'
    )
    end_time = models.TimeField(
        verbose_name='End Time'
    )
    summary = models.CharField(
        max_length=500,
        blank=True,
        verbose_name='Summary'
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Create Time',
        db_index=True
    )
    update_time = models.DateTimeField(
        auto_now=True,
        verbose_name='Update Time',
        db_index=True
    )

    class Meta:
        db_table = 'daily_schedules'
        verbose_name = 'Daily Schedule'
        verbose_name_plural = 'Daily Schedules'
        indexes = [
            models.Index(fields=['itinerary']),
            models.Index(fields=['day_number']),
            models.Index(fields=['create_time']),
            models.Index(fields=['update_time']),
        ]

    def __str__(self):
        return f"Day {self.day_number} of {self.itinerary}"


class POI(models.Model):
    poi_id = models.AutoField(primary_key=True)
    schedule = models.ForeignKey(   
        DailySchedule,
        on_delete=models.CASCADE,
        related_name='pois',
        verbose_name='Daily Schedule',
        db_index=True
    )
    name = models.CharField(
        max_length=255,
        verbose_name='Name'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Description'
    )
    category = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Category'
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Location'
    )
    target_audience = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Target Audience'
    )
    booking_link = models.CharField(
        max_length=500,
        blank=True,
        verbose_name='Booking Link'
    )
    avg_duration = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Average Duration (minutes)'
    )
    opening_hours = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Opening Hours'
    )
    ticket_price = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Ticket Price'
    )
    review_summary = models.TextField(
        blank=True,
        verbose_name='Review Summary'
    )
    review_source = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Review Source'
    )
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        null=True,
        blank=True,
        verbose_name='Rating'
    )
    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Create Time',
        db_index=True
    )
    update_time = models.DateTimeField(
        auto_now=True,
        verbose_name='Update Time',
        db_index=True
    )

    class Meta:
        db_table = 'poi'
        verbose_name = 'POI'
        verbose_name_plural = 'POIs'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
            models.Index(fields=['create_time']),
            models.Index(fields=['update_time']),
        ]

    def __str__(self):
        return self.name

