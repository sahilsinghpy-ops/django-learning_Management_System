from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):

    is_booking_open = serializers.BooleanField(read_only=True)

    class Meta:
        model = Event
        fields = [
            'id',
            'title',
            'description',
            'date',
            'location',
            'total_seats',
            'available_seats',
            'price_per_seat',
            'is_active',
            'is_booking_open',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['is_booking_open', 'created_at', 'updated_at']