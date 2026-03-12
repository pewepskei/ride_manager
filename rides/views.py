from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from django.db.models import Prefetch, F
from .models import Ride, RideEvent, User
from .serializers import RideSerializer
from .permissions import IsAdminUserRole
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rides.models import User
from rest_framework_simplejwt.tokens import RefreshToken

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

        last_24h = timezone.now() - timedelta(hours=24)
    
        ride_events_queryset = RideEvent.objects.filter(
            created_at__gte=last_24h
        ).only(
            'id_ride_event',
            'id_ride',
            'description',
            'created_at'
        )
    
        queryset = Ride.objects.select_related(
            'id_rider',
            'id_driver'
        ).only(
            'id_ride',
            'status',
            'pickup_latitude',
            'pickup_longitude',
            'dropoff_latitude',
            'dropoff_longitude',
            'pickup_time',
    
            'id_rider__id_user',
            'id_rider__first_name',
            'id_rider__last_name',
            'id_rider__email',
            'id_rider__role',
            'id_rider__phone_number',
    
            'id_driver__id_user',
            'id_driver__first_name',
            'id_driver__last_name',
            'id_driver__email',
            'id_driver__role',
            'id_driver__phone_number',
        ).prefetch_related(
            Prefetch(
                'ride_events',
                queryset=ride_events_queryset,
                to_attr='prefetched_events'
            )
        )
    
        # Filter by status
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
    
        # Filter by rider email
        rider_email = self.request.query_params.get('rider_email')
        if rider_email:
            queryset = queryset.filter(id_rider__email__icontains=rider_email)
    
        # Distance sorting
        lat = self.request.query_params.get('lat')
        lng = self.request.query_params.get('lng')
        
        if lat and lng:
            lat = float(lat)
            lng = float(lng)
        
            queryset = queryset.annotate(
                distance=ExpressionWrapper(
                    (F('pickup_latitude') - lat) * (F('pickup_latitude') - lat) +
                    (F('pickup_longitude') - lng) * (F('pickup_longitude') - lng),
                    output_field=FloatField()
                )
            ).order_by('distance')
        
        return queryset
