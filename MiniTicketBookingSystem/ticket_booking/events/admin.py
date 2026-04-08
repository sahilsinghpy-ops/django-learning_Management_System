from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'location', 'available_seats', 'price_per_seat', 'is_active']
    list_filter = ['is_active', 'date', 'location']
    search_fields = ['title', 'location']
    readonly_fields = ['available_seats']