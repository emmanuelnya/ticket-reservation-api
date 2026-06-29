from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "organizer", "date", "location", "seats_available", "seats_total"]
    list_filter = ["organizer"]
    search_fields = ["title", "location"]
