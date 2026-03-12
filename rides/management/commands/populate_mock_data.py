import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from rides.models import User, Ride, RideEvent


class Command(BaseCommand):
    help = "Populate large mock dataset efficiently"

    def add_arguments(self, parser):
        parser.add_argument(
            "--rides",
            type=int,
            default=100000,
            help="Number of rides to generate",
        )

    def handle(self, *args, **options):

        ride_count = options["rides"]
        batch_size = 5000
        now = timezone.now()

        self.stdout.write("Deleting existing data...")

        RideEvent.objects.all().delete()
        Ride.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write("Creating users...")

        users = []

        admin = User(
            id_user=1,
            role="admin",
            first_name="Admin",
            last_name="User",
            email="admin@test.com",
            phone_number="09000000000",
        )
        users.append(admin)

        for i in range(2, 52):
            users.append(
                User(
                    id_user=i,
                    role="rider",
                    first_name=f"Rider{i}",
                    last_name="Test",
                    email=f"rider{i}@test.com",
                    phone_number=f"091234567{i}",
                )
            )

        for i in range(52, 102):
            users.append(
                User(
                    id_user=i,
                    role="driver",
                    first_name=f"Driver{i}",
                    last_name="Test",
                    email=f"driver{i}@test.com",
                    phone_number=f"099876543{i}",
                )
            )

        User.objects.bulk_create(users)

        riders = [u for u in users if u.role == "rider"]
        drivers = [u for u in users if u.role == "driver"]

        self.stdout.write("Generating rides and ride events...")

        rides = []
        ride_events = []

        ride_id = 1
        ride_event_id = 1

        for _ in range(ride_count):

            rider = random.choice(riders)
            driver = random.choice(drivers)

            pickup_time = now - timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
            )

            # Trip duration between 20 mins and 90 mins
            trip_duration = random.randint(20, 90)

            # Pickup event happens shortly after ride creation
            pickup_event_time = pickup_time + timedelta(minutes=random.randint(1, 5))

            # Dropoff happens after trip duration
            dropoff_event_time = pickup_event_time + timedelta(minutes=trip_duration)

            ride = Ride(
                id_ride=ride_id,
                status="dropoff",
                id_rider=rider,
                id_driver=driver,
                pickup_latitude=14.5 + random.random() * 0.3,
                pickup_longitude=120.9 + random.random() * 0.3,
                dropoff_latitude=14.5 + random.random() * 0.3,
                dropoff_longitude=120.9 + random.random() * 0.3,
                pickup_time=pickup_time,
            )

            rides.append(ride)

            ride_events.append(
                RideEvent(
                    id_ride_event=ride_event_id,
                    id_ride=ride,
                    description="Status changed to pickup",
                    created_at=pickup_event_time,
                )
            )
            ride_event_id += 1

            ride_events.append(
                RideEvent(
                    id_ride_event=ride_event_id,
                    id_ride=ride,
                    description="Status changed to dropoff",
                    created_at=dropoff_event_time,
                )
            )
            ride_event_id += 1

            ride_id += 1

            if len(rides) >= batch_size:

                Ride.objects.bulk_create(rides)
                RideEvent.objects.bulk_create(ride_events)

                rides.clear()
                ride_events.clear()

                self.stdout.write(f"Inserted {ride_id} rides...")

        if rides:
            Ride.objects.bulk_create(rides)
            RideEvent.objects.bulk_create(ride_events)

        self.stdout.write(
            self.style.SUCCESS(f"Successfully generated {ride_count} rides")
        )
