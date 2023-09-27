from pets.models import Pet
from rest_framework import serializers
from services.models import BookingService, Service
from users.v1.serializers import SupplierProfileSerializer


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    supplier = SupplierProfileSerializer(read_only=True)

    class Meta:
        model = Service
        fields = (
            "supplier",
            "price",
            "work_time_from",
            "work_time_to",
            "about",
            "pet_type",
            "grooming_type",
            "duration",
            "published",
        )


class BookingServiceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BookingService
        fields = (
            "favour",
            "date",
            "place",
            "client",
            "supplier",
            "actual",
            "confirmed",
        )


