from django.contrib import admin

from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "room", "check_in", "check_out", "created_at")
    list_filter = ("check_in", "check_out", "created_at")
    search_fields = ("user__username", "room__number")
    date_hierarchy = "check_in"
