from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CustomUserCreateView, HydroponicSystemViewSet, MeasurementCreateView, MeasurementListView

router = DefaultRouter()
router.register(r'hydroponic-systems', HydroponicSystemViewSet)

urlpatterns = [
    path('register/', CustomUserCreateView.as_view(), name='user-register'),

    path('', include(router.urls)),

    path('measurements/', MeasurementListView.as_view(), name='measurement-list'),
    path('measurements/create/', MeasurementCreateView.as_view(), name='measurement-create'),
]
