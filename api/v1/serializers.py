from typing import Any

from rest_framework.exceptions import ValidationError
from rest_framework.relations import StringRelatedField, PrimaryKeyRelatedField

from core.utils import remove_dict_fields
from core.constants import Limits, Default


from pets.models import Pet, Age
from services.models import Schedule
from users.models import SupplierProfile, CustomerProfile
from users.v1.serializers import (
    BaseProfileSerializer,
    Base64ImageField,
    SupplierProfileSerializer,
)
from rest_framework import serializers
from services.models import BookingService, Service


class AgeSerializer(serializers.ModelSerializer):
    """Сериализация возраста."""

    class Meta:
        model = Age
        fields = (
            "year",
            "month",
        )

    def validate(self, data):
        if (
            data.get("year") > Limits.MAX_AGE_PET
            or data.get("year") < Limits.MIN_AGE_PET
        ):
            raise ValidationError(
                "Возраст питомца должен быть от "
                f"{Limits.MIN_AGE_PET} до {Limits.MAX_AGE_PET} лет"
            )
        if (
            data.get("month") < 0
            or data.get("month") > Limits.MAX_MONTH_QUANTITY
        ):
            raise ValidationError(
                f"Количество месяцев должно быть от 0 до 12."
            )


class PetSerializer(serializers.ModelSerializer):
    """Сериализация питомцев."""

    age = AgeSerializer(read_only=True)

    def validate(self, data):
        if Pet.objects.filter(
            name=data.get("name"),
            age=data.get("age"),
            breed=data.get("breed"),
            type=data.get("type"),
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
            "description",
            "schedule",
        )


class ServiceSerializer(BaseServiceSerializer):
    """Сериализация всех услуг."""

    class Meta(BaseServiceSerializer.Meta):
        fields = BaseServiceSerializer.Meta.fields + (
            "id",
            "specialist_type",
            "published",
        )

    @staticmethod
    def validate_price(data):
        """Проверка на валидность стоимости."""

        if data[0] < Limits.MIN_PRICE or data[0] > Limits.MAX_PRICE:
            raise ValidationError(
                f"Стоимость услуги должна быть от {Limits.MIN_PRICE} до "
                f"{Limits.MAX_PRICE} р."
            )

    def validate(self, data):
        """Проверяем уникальность услуги и тип пользователя."""

        name = data.get("name")
        user = self.context.get("request").user
        print(user)
        if Service.objects.filter(
            name=name,
            supplier=user.profile_id,
        ).exists():
            raise serializers.ValidationError("Такая услуга уже существует!")
        if not SupplierProfile.objects.filter(related_user=user).exists():
            raise serializers.ValidationError(
                "Услуги создает только специалист!"
            )
        return data


class FilterServicesSerializer(serializers.Serializer):
    price = serializers.ListField(
        required=False,
        child=serializers.IntegerField(
            min_value=Limits.MIN_PRICE, max_value=Limits.MAX_PRICE
        ),
        min_length=2,
        max_length=2,
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
        required=False, format=None, input_formats=("%d.%m.%Y",)
    )


class BaseBookingServiceSerializer(serializers.ModelSerializer):
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

class BookingServiceSerializer(BaseBookingServiceSerializer):
    service = serializers.PrimaryKeyRelatedField(queryset=Service.objects.all())
    def validate(self, data):
        service = data.get("service")
        if BookingService.objects.filter(
            service=service,
            customer=self.context.get("request").user.profile_id,
        ).exists():
            raise serializers.ValidationError("Такая бронь уже существует!")
        return data

class BookingServiceRetrieveSerializer(BaseBookingServiceSerializer):
    service = ServiceSerializer(read_only=True)


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
