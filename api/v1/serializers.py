from core.constants import Limits, Default
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from core.validators import validate_services
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


class FilterServicesSerializer(serializers.Serializer):
    price = serializers.ListField(
        required=False,
        child=serializers.IntegerField(
            min_value=Limits.MIN_PRICE, max_value=Limits.MAX_PRICE
        ),
        min_length=2, max_length=2,
    )
    service_type = serializers.ListField(
        required=False,
        child=serializers.CharField(max_length=Limits.MAX_LEN_SERVICE_TYPE),
        max_length=4,
    )
    pet_type = serializers.ChoiceField(
        required=False,
        choices=Default.PET_TYPE,
    )
    serve_at_supplier = serializers.BooleanField(required=False)
    serve_at_customer = serializers.BooleanField(required=False)
    date = serializers.DateField(
        required=False,
        format=None, input_formats=("%d.%m.%Y",)
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
