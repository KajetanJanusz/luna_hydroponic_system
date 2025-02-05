from rest_framework import serializers
from .models import CustomUser, HydroponicSystem, Measurement

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    

class HydroponicSystemSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = HydroponicSystem
        fields = ['name', 'description', 'system_type', 'plant_type', 'ph_level', 'ec_level', 'created_at', 'updated_at', 'owner']

    def validate_ph_level(self, value):
        if value < 0 or value > 14:
            raise serializers.ValidationError("pH level must be between 0 and 14.")
        return value

    def validate_ec_level(self, value):
        if value < 0:
            raise serializers.ValidationError("EC level cannot be negative.")
        return value

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['ph_level', 'water_temperature', 'tds_level']