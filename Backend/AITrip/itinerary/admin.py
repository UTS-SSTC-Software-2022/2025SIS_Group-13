from django.contrib import admin
from .models import Itinerary, DailySchedule, POI

# Register your models here.
admin.site.register(Itinerary)
admin.site.register(DailySchedule)
admin.site.register(POI)