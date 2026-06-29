"""
Comando di gestione Django per popolare il database con dati demo:
utenti (admin, organizer, attendee), eventi ed esempi di prenotazioni.

Uso:
    python manage.py seed_demo_data
"""

from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone
from rest_framework.authtoken.models import Token

from events.models import Event
from reservations.models import Reservation

User = get_user_model()


class Command(BaseCommand):
    help = "Popola il database con utenti, eventi e prenotazioni demo."

    def handle(self, *args, **options):
        self.stdout.write("Creazione dati demo in corso...")

        # ── Utenti demo ────────────────────────────────────────────────────
        admin_user = self._get_or_create_user(
            username="admin_demo",
            email="admin@demo.com",
            password="admin12345",
            role=User.Role.ORGANIZER,
            is_staff=True,
            is_superuser=True,
        )

        organizer = self._get_or_create_user(
            username="manager_demo",
            email="manager@demo.com",
            password="manager12345",
            role=User.Role.ORGANIZER,
        )

        attendee = self._get_or_create_user(
            username="user_demo",
            email="user@demo.com",
            password="user12345",
            role=User.Role.ATTENDEE,
        )

        # ── Eventi demo ────────────────────────────────────────────────────
        if not Event.objects.exists():
            e1 = Event.objects.create(
                title="Concerto Jazz al Parco",
                description="Una serata di musica jazz dal vivo nel parco cittadino.",
                location="Firenze, Parco delle Cascine",
                date=timezone.now() + timedelta(days=10),
                organizer=organizer,
                seats_total=100,
                seats_available=95,
            )
            e2 = Event.objects.create(
                title="Conferenza Tech 2026",
                description="Conferenza annuale su intelligenza artificiale e sviluppo software.",
                location="Firenze, Palazzo dei Congressi",
                date=timezone.now() + timedelta(days=20),
                organizer=organizer,
                seats_total=200,
                seats_available=180,
            )
            e3 = Event.objects.create(
                title="Mostra d'Arte Contemporanea",
                description="Esposizione di artisti emergenti fiorentini.",
                location="Firenze, Galleria degli Uffizi",
                date=timezone.now() + timedelta(days=5),
                organizer=organizer,
                seats_total=50,
                seats_available=48,
            )
            e4 = Event.objects.create(
                title="Workshop di Fotografia",
                description="Workshop pratico su tecniche di fotografia urbana.",
                location="Firenze, Piazza della Signoria",
                date=timezone.now() + timedelta(days=15),
                organizer=organizer,
                seats_total=30,
                seats_available=30,
            )

            # ── Prenotazioni demo (per user_demo) ───────────────────────────
            Reservation.objects.create(user=attendee, event=e1, seats_booked=5)
            Reservation.objects.create(user=attendee, event=e2, seats_booked=20)
            Reservation.objects.create(
                user=attendee, event=e3, seats_booked=2,
                status=Reservation.Status.CANCELLED,
            )
            # nota: e3 ha gi\u00e0 seats_available=48 (impostato sopra) per
            # simulare lo stato dopo l'annullamento di questa prenotazione.

            self.stdout.write(self.style.SUCCESS(
                f"Creati 4 eventi e 3 prenotazioni demo."
            ))
        else:
            self.stdout.write("Eventi gi\u00e0 presenti, salto la creazione.")

        self.stdout.write(self.style.SUCCESS("Dati demo creati con successo!"))
        self.stdout.write("")
        self.stdout.write("Account demo disponibili:")
        self.stdout.write("  admin_demo   / admin12345   (superuser + organizer)")
        self.stdout.write("  manager_demo / manager12345 (organizer)")
        self.stdout.write("  user_demo    / user12345    (attendee)")

    def _get_or_create_user(self, username, email, password, role, **extra):
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": email, "role": role, **extra},
        )
        if created:
            user.set_password(password)
            user.save()
        Token.objects.get_or_create(user=user)
        return user
