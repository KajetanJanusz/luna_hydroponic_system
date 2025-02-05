from .models import Measurement
from django_filters import rest_framework as django_filters

class MeasurementFilter(django_filters.FilterSet):
    timestamp_after = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    timestamp_before = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')
    ph_min = django_filters.NumberFilter(field_name='ph_level', lookup_expr='gte')
    ph_max = django_filters.NumberFilter(field_name='ph_level', lookup_expr='lte')
    temp_min = django_filters.NumberFilter(field_name='water_temperature', lookup_expr='gte')
    temp_max = django_filters.NumberFilter(field_name='water_temperature', lookup_expr='lte')
    tds_min = django_filters.NumberFilter(field_name='tds_level', lookup_expr='gte')
    tds_max = django_filters.NumberFilter(field_name='tds_level', lookup_expr='lte')

    class Meta:
        model = Measurement
        fields = ['timestamp_after', 'timestamp_before', 'ph_min', 'ph_max',
                 'temp_min', 'temp_max', 'tds_min', 'tds_max']