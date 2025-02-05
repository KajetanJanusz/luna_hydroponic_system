from rest_framework import viewsets, generics, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Prefetch
from django_filters import rest_framework as django_filters
from .filters import MeasurementFilter
from .models import CustomUser, HydroponicSystem, Measurement
from .serializers import CustomUserSerializer, HydroponicSystemSerializer, MeasurementSerializer

class CustomUserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]
    

class HydroponicSystemViewSet(viewsets.ModelViewSet):
    serializer_class = HydroponicSystemSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['name', 'created_at', 'updated_at', 'ph_level', 'ec_level']
    ordering = ['-created_at']

    def get_queryset(self):
        return HydroponicSystem.objects.filter(
            owner=self.request.user
        ).prefetch_related(
            Prefetch(
                'measurements',
                queryset=Measurement.objects.order_by('-timestamp')[:10],
                to_attr='recent_measurements'
            )
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def all_measurements(self, request, pk=None):
        system = self.get_object()
        measurements = system.measurements.all().order_by('-timestamp')
        page = self.paginate_queryset(measurements)
        
        if page is not None:
            serializer = MeasurementSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = MeasurementSerializer(measurements, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def latest_measurement(self, request, pk=None):
        system = self.get_object()
        measurement = system.measurements.order_by('-timestamp').first()
        
        if measurement:
            serializer = MeasurementSerializer(measurement)
            return Response(serializer.data)
        return Response({'detail': 'No measurements found'}, status=404)

class MeasurementCreateView(generics.CreateAPIView):
    serializer_class = MeasurementSerializer

class MeasurementListView(generics.ListAPIView):
    serializer_class = MeasurementSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    filter_backends = [
        django_filters.DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filterset_class = MeasurementFilter
    ordering_fields = ['timestamp', 'ph_level', 'water_temperature', 'tds_level']
    ordering = ['-timestamp']

    def get_queryset(self):
        return Measurement.objects.filter(
            hydroponic_system__owner=self.request.user
        ).select_related('hydroponic_system')