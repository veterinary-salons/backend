from typing import Any

from rest_framework.exceptions import ValidationError

from core.utils import remove_dict_fields
from core.validators import validate_services
from core.constants import Limits, Default


from pets.models import Pet
from services.models import Schedule
from users.models import SupplierProfile
from users.v1.serializers import (
    CustomerProfileSerializer,
    BaseProfileSerializer,
    Base64ImageField,
    SupplierProfileSerializer,
)
from rest_framework import serializers
from services.models import BookingService, Service


class PetSerializer(serializers.ModelSerializer):
    """Сериализация питомцев."""
    def validate(self, data):
        if Pet.objects.filter(
            name=data.get("name"),
            age=data.get("age"),
            breed = data.get("breed"),
            type = data.get("type"),
        ).exists():
            raise serializers.ValidationError("Такой питомец уже существует!")
        return data

    class Meta:
        model = Pet
        fields = "__all__"


class ScheduleSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = dict(super().to_representation(instance))
        for key in representation:
            if representation[key]:
                representation[key] = {"available": representation[key]}
            else:
                representation[key] = {"unavailable": representation[key]}
        return representation

    class Meta:
        model = Schedule
        fields = (
            "monday_hours",
            "tuesday_hours",
            "wednesday_hours",
            "thursday_hours",
            "friday_hours",
            "saturday_hours",
            "sunday_hours",
            "breakTime",
        )

class BaseServiceSerializer(serializers.ModelSerializer):
    """Сериализатор услуг для бронирования."""
    schedule = ScheduleSerializer(read_only=True)
    class Meta:
        model = Service
        fields = (
            "name",
            "pet_type",
            "price",
            "about",
            "grooming_type",
            "task",
            "formats",
            "schedule",
        )

class ServiceSerializer(serializers.ModelSerializer):
    """Сериализация всех услуг."""
    schedule = ScheduleSerializer(read_only=True)
    class Meta:
        model = Service
        fields = (
            "id",
            "name",
            "specialist_type",
            "schedule",
            "price",
            "about",
            "pet_type",
            "grooming_type",
            "duration",
            "task",
            "formats",
            "published",
        )
    def to_representation(self, instance) -> dict[str, Any]:
        representation = super().to_representation(instance)
    
        if representation.get("specialist_type") == "cynology":
            remove_dict_fields(representation, ["grooming_type", "pet_type"])
    
        if representation.get("specialist_type") == "veterenary":
            remove_dict_fields(
                representation, ["grooming_type", "formats", "task"]
            )
    
        if representation.get("specialist_type") == "grooming":
            remove_dict_fields(representation, ["formats", "task"])
    
        if representation.get("specialist_type") == "shelter":
            remove_dict_fields(
                representation, ["formats", "task", "grooming_type"]
            )
    
        return representation


    @staticmethod
    def validate_price(data):
        """Проверка на валидность стоимости."""

        if data[0] < Limits.MIN_PRICE or data[0] > Limits.MAX_PRICE:
            raise ValidationError(
                f"Стоимость услуги должна быть от {Limits.MIN_PRICE} до "
                f"{Limits.MAX_PRICE} р."
            )

    def validate(self, data):
        """Проверка на валидность услуги.

        Проверяем соответствие полей видам услуги и уникальность услуги.

        """
        service_type = data.get("service_type")
        pet_type = data.get("pet_type")
        task = data.get("task")
        formats = data.get("formats")
        grooming_type = data.get("grooming_type")
        name = data.get("name")
        validate_services(service_type, pet_type, task, formats, grooming_type)
        if Service.objects.filter(
            name=name,
            supplier=self.context.get("request").user.profile_id,
        ).exists():
            raise serializers.ValidationError("Такая услуга уже существует!")

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
    service = BaseServiceSerializer(read_only=True)
    supplier = SupplierProfileSerializer(read_only=True)

    class Meta:
        model = BookingService
        fields = (
            "to_date",
            "supplier",
            "service",
            "customer_place",
            "supplier_place",
        )

    def validate(self, data):
        service = data.get("service")
        if BookingService.objects.filter(
            favour=service,
            customer=self.context.get("request").user.profile_id,
        ).exists():
            raise serializers.ValidationError("Такая бронь уже существует!")
        return data


class SupplierSerializer(BaseProfileSerializer):
    photo = Base64ImageField(allow_null=True)
    service = ServiceSerializer(
        many=True, read_only=True, source="service_set"
    )

    class Meta:
        model = SupplierProfile
        fields = (
            "photo",
            "contact_email",
            "address",
            "phone_number",
            "user",
            "service",
        )
