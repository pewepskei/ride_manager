from django.db import models


class User(models.Model):
    id_user = models.IntegerField(primary_key=True)
    role = models.CharField(max_length=50)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.CharField(max_length=150, unique=True, db_index=True)
    phone_number = models.CharField(max_length=20)

    class Meta:
        db_table = "user"
        indexes = [
            models.Index(fields=["role"]),
        ]

    def __str__(self):
        return f"{self.email} ({self.role})"


class Ride(models.Model):
    id_ride = models.IntegerField(primary_key=True)

    status = models.CharField(max_length=50, db_index=True)

    id_rider = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="rides_as_rider"
    )

    id_driver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="rides_as_driver"
    )

    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()

    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()

    pickup_time = models.DateTimeField(db_index=True)

    class Meta:
        db_table = "ride"
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["pickup_time"]),
        ]

    def __str__(self):
        return f"Ride {self.id_ride} ({self.status})"


class RideEvent(models.Model):
    id_ride_event = models.AutoField(primary_key=True)

    id_ride = models.ForeignKey(
        Ride,
        related_name="ride_events",
        on_delete=models.CASCADE
    )

    description = models.TextField()

    created_at = models.DateTimeField(db_index=True)

    class Meta:
        db_table = "ride_event"
        indexes = [
            models.Index(fields=["id_ride", "created_at"]),
        ]

    def __str__(self):
        return f"RideEvent {self.id_ride_event} for Ride {self.id_ride_id}"
