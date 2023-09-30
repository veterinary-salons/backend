from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from core.validators import validate_services
from pets.models import Pet
from rest_framework import serializers, status
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
            "name",
            "supplier",
            "price",
            "work_time_from",
            "work_time_to",
            "about",
            "pet_type",
            "grooming_type",
            "duration",
            "task",
            "formats",
            "published",
        )

    def validate(self, data):
        name = data.get("name")
        pet_type = data.get("pet_type")
        task = data.get("task")
        formats = data.get("formats")
        grooming_type = data.get("grooming_type")
        validate_services(name, pet_type, task, formats, grooming_type)
        if Service.objects.filter(
            name=name, supplier=self.context.get("request").user.profile_id
        ).exists():
            raise serializers.ValidationError(
                "Такая услуга уже существует!"
            )

        return data


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
