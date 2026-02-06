from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .serializers import UserRegistrationSerializer, BookingSerializer
from django.contrib.auth.models import User
from .models import Booking
from rooms.models import Room
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='check_in',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description='Check-in date (YYYY-MM-DD)',
                required=True
            ),
            OpenApiParameter(
                name='check_out',
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description='Check-out date (YYYY-MM-DD)',
                required=True
            ),
            OpenApiParameter(
                name='capacity',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description='Minimum room capacity',
                required=False
            ),
        ],
        description='Search for available rooms in a given date range'
    )
    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def available_rooms(self, request):
        check_in = request.query_params.get('check_in')
        check_out = request.query_params.get('check_out')
        capacity = request.query_params.get('capacity')

        if not check_in or not check_out:
            return Response(
                {"error": "Please provide check_in and check_out dates"},
                status=status.HTTP_400_BAD_REQUEST
            )

        booked_rooms_ids = Booking.objects.filter(
            check_in__lt=check_out,
            check_out__gt=check_in
        ).values_list('room_id', flat=True)

        available_rooms = Room.objects.exclude(id__in=booked_rooms_ids)

        if capacity:
            available_rooms = available_rooms.filter(capacity__gte=capacity)

        from rooms.serializers import RoomSerializer
        serializer = RoomSerializer(available_rooms, many=True)
        return Response(serializer.data)
