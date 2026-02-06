from django.contrib import admin
from .models import Room

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'price_per_night', 'capacity', 'updated_at')
    search_fields = ('number',)
    list_filter = ('capacity', 'created_at')
    ordering = ('number',)
