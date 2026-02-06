from django.db import models


class Room(models.Model):
    number = models.CharField(max_length=50, unique=True, verbose_name="Room Number")
    price_per_night = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Price per Night"
    )
    capacity = models.PositiveIntegerField(verbose_name="Capacity (Guests)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["number"]
        verbose_name = "Room"
        verbose_name_plural = "Rooms"

    def __str__(self) -> str:
        return (
            f"Room {self.number} ({self.capacity} ppl) - {self.price_per_night}/night"
        )
