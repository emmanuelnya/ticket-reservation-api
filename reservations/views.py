from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Reservation
from .permissions import IsOwner
from .serializers import ReservationSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    """
    ViewSet completo (class-based) per la risorsa Reservation.

    Endpoint generati automaticamente dal router:
      GET    /api/reservations/            -> lista SOLO le proprie prenotazioni
      POST   /api/reservations/            -> crea una prenotazione (utente autenticato)
      GET    /api/reservations/{id}/       -> dettaglio (solo proprietario)
      PUT    /api/reservations/{id}/       -> aggiorna (solo proprietario)
      PATCH  /api/reservations/{id}/       -> aggiorna parzialmente (solo proprietario)
      DELETE /api/reservations/{id}/       -> elimina (solo proprietario)
      POST   /api/reservations/{id}/cancel/ -> azione custom: annulla e libera i posti
    """

    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Ogni utente vede e gestisce solo le proprie prenotazioni.
        return Reservation.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        """
        Annulla una prenotazione confermata e restituisce i posti
        liberati all'evento collegato.
        """
        reservation = self.get_object()
        if reservation.status == Reservation.Status.CANCELLED:
            return Response({"detail": "La prenotazione è già annullata."}, status=400)

        reservation.status = Reservation.Status.CANCELLED
        reservation.save(update_fields=["status"])

        event = reservation.event
        event.seats_available += reservation.seats_booked
        event.save(update_fields=["seats_available"])

        return Response(ReservationSerializer(reservation).data)
