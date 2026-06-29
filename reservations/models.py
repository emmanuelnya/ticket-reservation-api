from django.conf import settings
from django.db import models


class Reservation(models.Model):
    """
    Rappresenta la prenotazione di uno o più posti per un evento.

    Relazioni:
      - Reservation -> User  (ForeignKey su chi ha prenotato)
      - Reservation -> Event (ForeignKey sull'evento prenotato)
    """

    class Status(models.TextChoices):
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reservations",
    )
    event = models.ForeignKey(
        "events.Event",
        on_delete=models.CASCADE,
        related_name="reservations",
    )
    seats_booked = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.CONFIRMED
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.user.username} -> {self.event.title} ({self.status})"
