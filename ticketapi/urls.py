"""
URL principali del progetto ticketapi.
Tutti gli endpoint dell'API sono raggruppati sotto il prefisso /api/.
"""

from django.contrib import admin
from django.urls import include, path
from django.http import JsonResponse


def api_root(request):
    return JsonResponse({
        "message": "Ticket Reservation API – TravelBus/Eventi",
        "endpoints": {
            "admin": "/admin/",
            "register": "/api/auth/register/",
            "login": "/api/auth/login/",
            "me": "/api/auth/me/",
            "events": "/api/events/",
            "reservations": "/api/reservations/",
        },
    })


urlpatterns = [
    path("", api_root),
    path("admin/", admin.site.urls),
    path("api/", include("accounts.urls")),
    path("api/", include("events.urls")),
    path("api/", include("reservations.urls")),
]
