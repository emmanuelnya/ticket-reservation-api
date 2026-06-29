from django.conf import settings
from django.db import models


class Event(models.Model):
    """
    Rappresenta un evento che può essere prenotato dagli utenti.

    Relazione: Event -> User (organizer) tramite ForeignKey.
    """

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    date = models.DateTimeField(help_text="Data e ora dell'evento.")
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="events",
        help_text="Utente con ruolo ORGANIZER che ha creato l'evento.",
    )
    seats_total = models.PositiveIntegerField(default=50)
    seats_available = models.PositiveIntegerField(default=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["date"]

    def __str__(self) -> str:
        return f"{self.title} ({self.date:%d/%m/%Y})"
