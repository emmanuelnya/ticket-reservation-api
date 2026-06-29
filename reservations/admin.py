from django.contrib import admin

from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ["user", "event", "seats_booked", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["user__username", "event__title"]
