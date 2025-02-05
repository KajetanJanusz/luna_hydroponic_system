from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from .models import CustomUser, HydroponicSystem, Measurement
from .serializers import CustomUserSerializer, HydroponicSystemSerializer, MeasurementSerializer

class CustomUserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]
    

class HydroponicSystemViewSet(viewsets.ModelViewSet):
    queryset = HydroponicSystem.objects.all()
    serializer_class = HydroponicSystemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HydroponicSystem.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class MeasurementCreateView(generics.CreateAPIView):
    serializer_class = MeasurementSerializer

class MeasurementListView(generics.ListAPIView):
    serializer_class = MeasurementSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Measurement.objects.filter(hydroponic_system__owner=self.request.user)
    