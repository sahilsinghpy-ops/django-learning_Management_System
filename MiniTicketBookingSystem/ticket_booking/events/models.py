from django.db import models
from django.core.validators import MinValueValidator


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    total_seats = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    # Yeh line change kar do
    available_seats = models.PositiveIntegerField(
        validators=[MinValueValidator(0)],
        default=0  # ← Yeh important hai
    )

    price_per_seat = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.date.strftime('%d %b %Y')}"