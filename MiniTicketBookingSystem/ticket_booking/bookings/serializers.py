from rest_framework import serializers
from .models import Booking
from events.models import Event  # ← Model import kiya
from events.serializers import EventSerializer


class BookingSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)

    event_id = serializers.PrimaryKeyRelatedField(
        queryset=Event.objects.filter(is_active=True),  # ← Ab sahi hai
        source='event',
        write_only=True
    )

    class Meta:
        model = Booking
        fields = ['id', 'event', 'event_id', 'seats_booked', 'total_price',
                  'status', 'booking_date']
        read_only_fields = ['total_price', 'status']

    def validate(self, data):
        event = data.get('event')
        if not event:
            raise serializers.ValidationError({"error": "Event is required."})

        requested_seats = data.get('seats_booked', 0)

        if requested_seats > event.available_seats:
            raise serializers.ValidationError({"error": "Not enough seats available."})

        if not event.is_active or event.available_seats <= 0:
            raise serializers.ValidationError({"error": "Booking is closed for this event."})

        return data