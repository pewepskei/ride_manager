from rest_framework import serializers
from .models import Ride, RideEvent, User
from django.utils import timezone
from datetime import timedelta

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id_user', 'first_name', 'last_name', 'email', 'role']

class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = ['id_ride_event', 'description', 'created_at']

class RideSerializer(serializers.ModelSerializer):
    id_rider = UserSerializer()
    id_driver = UserSerializer()
    todays_ride_events = serializers.SerializerMethodField()

    class Meta:
        model = Ride
        fields = ['id_ride', 'status', 'id_rider', 'id_driver',
                  'pickup_latitude', 'pickup_longitude', 'dropoff_latitude', 'dropoff_longitude',
                  'pickup_time', 'todays_ride_events']

    def get_todays_ride_events(self, ride):
        last_24_hours = timezone.now() - timedelta(hours=24)
        events = ride.ride_events.filter(created_at__gte=last_24_hours)
        return RideEventSerializer(events, many=True).data
