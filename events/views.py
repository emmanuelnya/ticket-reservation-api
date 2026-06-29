from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from reservations.serializers import ReservationSerializer

from .models import Event
from .permissions import IsOrganizerOrReadOnly
from .serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet completo (class-based) per la risorsa Event.

    Endpoint generati automaticamente dal router:
      GET    /api/events/            -> lista eventi (pubblico)
      POST   /api/events/            -> crea evento (solo ORGANIZER)
      GET    /api/events/{id}/       -> dettaglio evento (pubblico)
      PUT    /api/events/{id}/       -> aggiorna evento (solo organizer proprietario)
      PATCH  /api/events/{id}/       -> aggiorna parzialmente (solo organizer proprietario)
      DELETE /api/events/{id}/       -> elimina evento (solo organizer proprietario)
      GET    /api/events/{id}/attendees/ -> azione custom, solo organizer proprietario
    """

    queryset = Event.objects.all().order_by("date")
    serializer_class = EventSerializer
    permission_classes = [IsOrganizerOrReadOnly]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    @action(detail=True, methods=["get"], permission_classes=[permissions.IsAuthenticated])
    def attendees(self, request, pk=None):
        """
        Endpoint specifico per ruolo (ORGANIZER): restituisce l'elenco
        delle prenotazioni confermate per l'evento, visibile solo
        all'organizer proprietario dell'evento.
        """
        event = self.get_object()
        if event.organizer_id != request.user.id:
            return Response(
                {"detail": "Solo l'organizer di questo evento può vedere gli iscritti."},
                status=403,
            )
        reservations = event.reservations.filter(status="CONFIRMED")
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)
