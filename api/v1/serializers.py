from core.validators import validate_services
from pets.models import Pet
from rest_framework import serializers
from services.models import BookingService, Service, Schedule
from users.models import SupplierProfile
from users.v1.serializers import (
    CustomerProfileSerializer,
    BaseProfileSerializer,
    Base64ImageField,
)


class PetSerializer(serializers.ModelSerializer):
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


class ServiceSerializer(serializers.ModelSerializer):
    # supplier = SupplierProfileSerializer(read_only=True)
    schedule = ScheduleSerializer(read_only=True)
    class Meta:
        model = Service
        fields = (
            "id",
            "name",
            "specialist_type",
            # "supplier",
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

    def validate(self, data):
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


class BookingServiceSerializer(serializers.ModelSerializer):
    service = serializers.CharField(source="favour")
    customer = CustomerProfileSerializer(read_only=True)

    class Meta:
        model = BookingService
        fields = (
            "service",
            "date",
            "to_date",
            "place",
            "customer",
            "supplier",
            "actual",
            "is_done",
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
            "customer_place",
            "supplier_place",
        )
