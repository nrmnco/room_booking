from rest_framework import serializers
from .models import Room

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'number', 'price_per_night', 'capacity', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
