from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('customer', 'Customer'),
        ('event_manager', 'Event Manager'),
    )

    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='customer'
    )
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

    @property
    def is_event_manager(self):
        return self.user_type == 'event_manager'

    @property
    def is_customer(self):
        return self.user_type == 'customer'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'