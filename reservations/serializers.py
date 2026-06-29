from rest_framework import serializers

from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    """
    Serializer per la risorsa Reservation.

    Valida che:
      - seats_booked sia maggiore di 0;
      - l'evento abbia posti disponibili sufficienti.
    Alla creazione, decrementa automaticamente seats_available
    sull'evento collegato e imposta lo user sull'utente autenticato.
    """

    event_title = serializers.ReadOnlyField(source="event.title")
    username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Reservation
        fields = [
            "id", "user", "username", "event", "event_title",
            "seats_booked", "status", "created_at",
        ]
        read_only_fields = ["user", "status", "created_at"]

    def validate(self, attrs):
        event = attrs.get("event")
        seats_booked = attrs.get("seats_booked", 1)

        if seats_booked <= 0:
            raise serializers.ValidationError(
                {"seats_booked": "Devi prenotare almeno 1 posto."}
            )
        if event and event.seats_available < seats_booked:
            raise serializers.ValidationError(
                {"event": f"Posti disponibili insufficienti ({event.seats_available} rimasti)."}
            )
        return attrs

    def create(self, validated_data):
        event = validated_data["event"]
        seats_booked = validated_data.get("seats_booked", 1)

        event.seats_available -= seats_booked
        event.save(update_fields=["seats_available"])

        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
