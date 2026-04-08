from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    event = models.ForeignKey(
        'events.Event',  # ← String reference use kiya (best practice)
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    seats_booked = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )

    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        editable=False
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    booking_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-booking_date']

    def __str__(self):
        return f"{self.user.username} - {self.event.title} ({self.seats_booked} seats)"

    def save(self, *args, **kwargs):
        if not self.total_price and self.event:
            self.total_price = self.seats_booked * self.event.price_per_seat
        super().save(*args, **kwargs)