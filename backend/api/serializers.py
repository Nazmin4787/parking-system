from rest_framework import serializers
from .models import User, ParkingSlot, Booking

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'password']
    

    def validate_username(self, value):
        # Bypass uniqueness validation temporarily
        return value
    
    def validate_email(self, value):
        # Bypass uniqueness validation temporarily
        return value
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user

class ParkingSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSlot
        fields = ['id', 'slot_number', 'floor', 'is_occupied']

class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'slot', 'start_time', 'end_time', 'is_active']
        read_only_fields = ['user', 'start_time']           

        