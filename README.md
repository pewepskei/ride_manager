# Wingz Exam

# Setup Instructions

## 1. Clone the Repository

```bash
git clone git@github.com:pewepskei/ride_manager.git
```

## 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Run Database Migrations

```bash
python manage.py migrate
```

## 5. Populate Database

```bash
python manage.py populate_mock_data
```

## 6. Start the Development Server

```bash
python manage.py runserver
```

API will be available at:

```
http://localhost:8000/
```

# Ride List API

## Endpoint
```
GET /api/rides/
```

## Headers
```
X-User-Email: admin@test.com
X-User-Role: admin
```

Example
```bash
curl http://localhost:8000/api/rides/ \
-H "X-User-Email: admin@test.com" \
-H "X-User-Role: admin"
```

## Query Parameters

| Parameter   | Description |
|-------------|-------------|
| page        | Page number |
| page_size   | Number of rides per page |
| status      | Filter by ride status (`pickup`, `en-route`, `dropoff`) |
| rider_email | Filter by rider email |
| ordering    | Sort by pickup time (`pickup_time`, `-pickup_time`) |
| lat         | Latitude used for distance sorting |
| lng         | Longitude used for distance sorting |

Examples

## Pagination
```
/api/rides/?page=1&page_size=10
```

## Filter by status
```
/api/rides/?status=en-route
```

## Filter by rider email
```
/api/rides/?rider_email=rider1@test.com
```

## Sort by pickup time
```
/api/rides/?ordering=-pickup_time
```

## Sort by distance
```
/api/rides/?lat=14.5995&lng=120.9842
```

## Combined example
```
/api/rides/?status=en-route&lat=14.5995&lng=120.9842&page_size=5
```

# Bonus SQL Query

The following SQL query calculates the **monthly count of rides longer than one hour per driver**.

```sql
SELECT 
    DATE_TRUNC('month', pickup.created_at) AS month,
    u.first_name || ' ' || u.last_name AS driver_name,
    COUNT(*) AS long_trip_count
FROM ride r
JOIN ride_event pickup
    ON pickup.id_ride_id = r.id_ride
    AND pickup.description = 'Status changed to pickup'
JOIN ride_event dropoff
    ON dropoff.id_ride_id = r.id_ride
    AND dropoff.description = 'Status changed to dropoff'
JOIN "user" u
    ON u.id_user = r.id_driver_id
WHERE dropoff.created_at - pickup.created_at > INTERVAL '1 hour'
GROUP BY month, driver_name
ORDER BY month, driver_name;
```

This query:
- Finds the pickup and dropoff events for each ride
- Calculates trip duration
- Counts trips longer than 1 hour
- Groups the results by month and driver
