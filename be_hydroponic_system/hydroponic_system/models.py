from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=13, blank=True, null=True)

    def __str__(self):
        return self.username


class HydroponicSystem(models.Model):
    SYSTEM_TYPES = [
        ('DWC', 'Deep Water Culture'),
        ('NFT', 'Nutrient Film Technique'),
        ('EBB', 'Ebb and Flow'),
        ('DRIP', 'Drip System'),
        ('AERO', 'Aeroponics'),
        ('WICK', 'Wick System'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    system_type = models.CharField(
        max_length=4,
        choices=SYSTEM_TYPES,
        default='DWC'
    )
    plant_type = models.CharField(max_length=50)
    ph_level = models.FloatField()
    ec_level = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Measurement(models.Model):
    hydroponic_system = models.ForeignKey(HydroponicSystem, on_delete=models.CASCADE, related_name="measurements")
    ph_level = models.FloatField()
    water_temperature = models.FloatField()
    tds_level = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Measurement for {self.hydroponic_system.name} at {self.timestamp}"