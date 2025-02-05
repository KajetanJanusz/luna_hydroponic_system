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
    measurements = serializers.SerializerMethodField()

    class Meta:
        model = HydroponicSystem
        fields = ['id', 'name', 'description', 'system_type', 'plant_type', 
                 'ph_level', 'ec_level', 'created_at', 'updated_at', 
                 'owner', 'measurements']

    def validate_ph_level(self, value):
        if value < 0 or value > 14:
            raise serializers.ValidationError("pH level must be between 0 and 14.")
        return value

    def validate_ec_level(self, value):
        if value < 0:
            raise serializers.ValidationError("EC level cannot be negative.")
        return value

    def get_measurements(self, obj):
        measurements = getattr(obj, 'recent_measurements', [])
        return MeasurementSerializer(measurements, many=True).data

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['ph_level', 'water_temperature', 'tds_level', 'timestamp']

    def validate_ph_level(self, value):
        if value < 0 or value > 14:
            raise serializers.ValidationError("pH level must be between 0 and 14.")
        return value

    def validate_water_temperature(self, value):
        if value <= 0:
            raise serializers.ValidationError("Water temperature cannot be less or eqaul to 0.")
        return value
    
    def validate_tds(self, value):
        if value < 0:
            raise serializers.ValidationError("Total Dissolved Solids cannot be less or eqaul to 0.")
        return value