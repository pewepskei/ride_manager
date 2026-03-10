from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django.db.models import Prefetch, F
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from .models import Ride, RideEvent, User
from .serializers import RideSerializer
from .permissions import IsAdminUserRole
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta

class RidePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'

class RideViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RideSerializer
    permission_classes = [IsAdminUserRole]
    pagination_class = RidePagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['id_rider__email', 'status']
    ordering_fields = ['pickup_time']

    def get_queryset(self):
        queryset = Ride.objects.select_related('id_rider', 'id_driver').all()

        # Filter by status
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)

        # Filter by rider email
        rider_email = self.request.query_params.get('rider_email')
        if rider_email:
            queryset = queryset.filter(id_rider__email__icontains=rider_email)

        # Optional: distance sorting (assuming lat/lng input)
        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')
        if lat and lng:
            from django.db.models import Func, F, FloatField
            # Approximate distance using Haversine formula in SQL
            lat = float(lat)
            lng = float(lng)
            queryset = queryset.annotate(
                distance=((F('pickup_latitude') - lat) ** 2 + (F('pickup_longitude') - lng) ** 2)
            ).order_by('distance')

        # Prefetch only last 24h ride events
        last_24h = timezone.now() - timedelta(hours=24)
        queryset = queryset.prefetch_related(
            Prefetch('ride_events', queryset=RideEvent.objects.filter(created_at__gte=last_24h))
        )
        return queryset
