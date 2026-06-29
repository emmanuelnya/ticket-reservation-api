from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Modello utente personalizzato per il Ticket Reservation API.

    Estende AbstractUser aggiungendo un campo `role` che determina
    i permessi dell'utente nel sistema:
      - ATTENDEE  : utente standard, gestisce le proprie prenotazioni.
      - ORGANIZER : crea e gestisce i propri eventi.
    """

    class Role(models.TextChoices):
        ATTENDEE = "ATTENDEE", "Attendee"
        ORGANIZER = "ORGANIZER", "Organizer"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ATTENDEE,
        help_text="Ruolo dell'utente: ATTENDEE o ORGANIZER.",
    )

    @property
    def is_organizer(self) -> bool:
        return self.role == self.Role.ORGANIZER

    @property
    def is_attendee(self) -> bool:
        return self.role == self.Role.ATTENDEE

    def __str__(self) -> str:
        return f"{self.username} ({self.role})"
