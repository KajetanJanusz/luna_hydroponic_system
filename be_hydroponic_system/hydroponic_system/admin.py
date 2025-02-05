from django.contrib import admin
from .models import CustomUser, HydroponicSystem, Measurement

admin.site.register(CustomUser)
admin.site.register(HydroponicSystem)
admin.site.register(Measurement)
