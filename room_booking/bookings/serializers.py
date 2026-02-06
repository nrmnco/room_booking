from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from .models import Booking
from django.conf import settings

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'room', 'check_in', 'check_out', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        check_in = data['check_in']
        check_out = data['check_out']
        room = data['room']

        if check_in >= check_out:
            raise serializers.ValidationError("Check-out date must be after check-in date.")

        if check_in < timezone.now().date():
            raise serializers.ValidationError("Cannot book in the past.")

        duration = (check_out - check_in).days
        min_days = getattr(settings, 'MIN_BOOKING_DAYS', 1)
        max_days = getattr(settings, 'MAX_BOOKING_DAYS', 30)

        if duration < min_days:
            raise serializers.ValidationError(f"Minimum booking duration is {min_days} day(s).")
        if duration > max_days:
            raise serializers.ValidationError(f"Maximum booking duration is {max_days} days.")

        existing_bookings = Booking.objects.filter(
            room=room,
            check_in__lt=check_out,
            check_out__gt=check_in
        )

        if self.instance:
            existing_bookings = existing_bookings.exclude(pk=self.instance.pk)

        if existing_bookings.exists():
            raise serializers.ValidationError("This room is already booked for the selected dates.")

        return data
