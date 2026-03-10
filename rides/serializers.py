from rest_framework import serializers
from .models import Ride, RideEvent, User


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

    # Use prefetched events instead of querying again
    todays_ride_events = RideEventSerializer(
        many=True,
        read_only=True,
        source='prefetched_events'
    )

    class Meta:
        model = Ride
        fields = [
            'id_ride',
            'status',
            'id_rider',
            'id_driver',
            'pickup_latitude',
            'pickup_longitude',
            'dropoff_latitude',
            'dropoff_longitude',
            'pickup_time',
            'todays_ride_events'
        ]
