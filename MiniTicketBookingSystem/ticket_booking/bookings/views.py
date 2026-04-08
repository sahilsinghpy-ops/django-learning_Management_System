from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db import transaction
from .models import Booking
from .serializers import BookingSerializer
from events.models import Event

from .permissions import IsCustomer


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated ,IsCustomer]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).select_related('event')

    # Custom create method with atomic transaction + race condition handling
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            event = serializer.validated_data['event']
            requested_seats = serializer.validated_data['seats_booked']

            # 🔥 Race Condition Fix: Lock the event row
            event = Event.objects.select_for_update().get(id=event.id)

            # Double validation after locking
            if requested_seats > event.available_seats:
                return Response(
                    {"error": "Not enough seats available right now. Please try again."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not event.is_active:
                return Response(
                    {"error": "Booking is closed for this event."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Create booking
            booking = serializer.save(user=request.user)

            # Reduce available seats
            event.available_seats -= requested_seats
            event.save()

            # Return full booking details
            response_serializer = BookingSerializer(booking)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Extra action: Cancel booking (baad mein use kar sakte hain)
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.user != request.user:
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

        if booking.status == 'cancelled':
            return Response({"error": "Booking already cancelled"}, status=status.HTTP_400_BAD_REQUEST)

        booking.status = 'cancelled'
        booking.save()

        # Optional: seats wapas add kar sakte ho
        # booking.event.available_seats += booking.seats_booked
        # booking.event.save()

        return Response({"message": "Booking cancelled successfully"}, status=status.HTTP_200_OK)