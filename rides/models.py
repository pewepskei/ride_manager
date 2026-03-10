from django.db import models

class User(models.Model):
    id_user = models.IntegerField(primary_key=True)
    role = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=20)

    class Meta:
        db_table = 'user'

class Ride(models.Model):
    id_ride = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=50)
    id_rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides_as_rider')
    id_driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rides_as_driver')
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField()

    class Meta:
        db_table = 'ride'

class RideEvent(models.Model):
    id_ride_event = models.IntegerField(primary_key=True)
    id_ride = models.ForeignKey(Ride, on_delete=models.CASCADE, related_name='ride_events')
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'ride_event'
