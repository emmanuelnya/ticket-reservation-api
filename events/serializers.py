from django.utils import timezone
from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    """
    Serializer per la risorsa Event.

    Valida che la data dell'evento sia futura e che seats_total sia
    positivo. Al momento della creazione, seats_available viene
    inizializzato pari a seats_total e l'organizer viene impostato
    automaticamente sull'utente autenticato.
    """

    organizer_username = serializers.ReadOnlyField(source="organizer.username")

    class Meta:
        model = Event
        fields = [
            "id", "title", "description", "location", "date",
            "organizer", "organizer_username",
            "seats_total", "seats_available", "created_at",
        ]
        read_only_fields = ["organizer", "seats_available", "created_at"]

    def validate_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("La data dell'evento deve essere futura.")
        return value

    def validate_seats_total(self, value):
        if value <= 0:
            raise serializers.ValidationError("seats_total deve essere maggiore di 0.")
        return value

    def create(self, validated_data):
        validated_data["seats_available"] = validated_data["seats_total"]
        validated_data["organizer"] = self.context["request"].user
        return super().create(validated_data)
