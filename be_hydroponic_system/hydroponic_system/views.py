from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import CustomUser, HydroponicSystem
from .serializers import CustomUserSerializer, HydroponicSystemSerializer

class HydroponicSystemViewSet(viewsets.ModelViewSet):
    queryset = HydroponicSystem.objects.all()
    serializer_class = HydroponicSystemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HydroponicSystem.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CustomUserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]