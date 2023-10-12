from copy import deepcopy

from django.core.exceptions import ValidationError
from icecream import ic
from rest_framework import serializers

from core.constants import Limits, Default
from pets.models import Pet, Age
from services.models import Booking, Service
from services.models import Schedule
from users.models import SupplierProfile, CustomerProfile
from users.v1.serializers import (
    BaseProfileSerializer,
    Base64ImageField,
    SupplierProfileSerializer,
    SupplierSerializer,
)


class AgeSerializer(serializers.ModelSerializer):
    """Сериализация возраста."""

    class Meta:
        model = Age
        fields = (
            "id",
            "year",
            "month",
        )

    @staticmethod
    def validate_year(value):
        if value > Limits.MAX_AGE_PET or value < Limits.MIN_AGE_PET:
            raise ValidationError(
                "Возраст питомца должен быть от "
                f"{Limits.MIN_AGE_PET} до {Limits.MAX_AGE_PET} лет"
            )
        return value

    @staticmethod
    def validate_month(value):
        if value > Limits.MAX_MONTH_QUANTITY or value < 0:
            raise ValidationError(
                "Месяц возраста питомца должен быть от "
                f"0 до {Limits.MAX_MONTH_QUANTITY} месяцев"
            )
        return value

class BasePetSerializer(serializers.ModelSerializer):
    """Сериализация питомцев."""

    weight = serializers.DecimalField(
        max_digits=4,
        decimal_places=1,
        required=False,
    )
    age = AgeSerializer(required=True)

    def create(self, validated_data):
        """Создание нового питомца."""
        ic(validated_data)
        age_data = validated_data.pop("age")
        age_serializer = AgeSerializer(data=age_data)
        age_serializer.is_valid(raise_exception=True)
        if Age.objects.filter(**age_data).exists():
            age = Age.objects.filter(**age_data).first()
        else:
            age = Age.objects.create(**age_data)
        return Pet.objects.create(age=age, **validated_data)


    def update(self, instance, validated_data):
        """Обновление питомца."""
        age_serializer = AgeSerializer(data=validated_data.get("age"))
        age_serializer.is_valid(raise_exception=True)
        validated_data["age"] = Age.objects.get_or_create(
            **validated_data.get("age")
        )[0]
        instance.age = validated_data["age"]
        return super().update(instance, validated_data)

    class Meta:
        model = Pet
        fields = (
            "name",
            "breed",
            "type",
            "age",
            "weight",
            "owner",
            "is_sterilized",
            "is_vaccinated",
        )

class PetSerializer(BasePetSerializer):
    """Сериализация питомцев с валидацией."""
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate(self, data):
        age = AgeSerializer(data=data.get("age"))
        age.is_valid(raise_exception=True)
        if Pet.objects.filter(
            name=data.get("name"),
            age__year=age.validated_data.get("year"),
            age__month=age.validated_data.get("month"),
            breed=data.get("breed"),
            type=data.get("type"),
        ).exists():
            raise serializers.ValidationError("Такой питомец уже существует!")
        return data


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
    booking = serializers.PrimaryKeyRelatedField(
        required=False,
        default=False,
        read_only=True,
    )

    class Meta:
        model = Service
        fields = (
            "id",
            "name",
            "pet_type",
            "price",
            "description",
            "schedule",
            "booking",
        )


class ServiceSerializer(BaseServiceSerializer):
    """Сериализация всех услуг."""
    supplier = SupplierSerializer(read_only=True)

    class Meta(BaseServiceSerializer.Meta):
        fields = BaseServiceSerializer.Meta.fields + (
            "specialist_type",
            "published",
            "supplier",
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


class BaseBookingSerializer(serializers.ModelSerializer):
    supplier = SupplierProfileSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = (
            "to_date",
            "customer_place",
            "supplier_place",
            "pet",
        )

class BookingSerializer(BaseBookingSerializer):
    booking_services = BaseServiceSerializer(
        many=True,
    )
    pet = BasePetSerializer()

    def create(self, validated_data, **kwargs):
        """Создание бронирования.

        Обрабатываем вложенные поля service и pet и вложенное в pet age.

        """
        booking_services_data = validated_data.pop("booking_services")
        pet_data = validated_data.pop("pet")
        age = Age.objects.get_or_create(**pet_data.pop("age"))
        pet_data.update(
            {
                "age": age[0],
                "owner": CustomerProfile.objects.get(
                    related_user=self.context.get("request").user
                ),
            }
        )
        pet, _ = Pet.objects.get_or_create(**pet_data)

        validated_data.update({"pet_id": pet.id})
        booking_service = Booking.objects.create(**validated_data)
        supplier = SupplierProfile.objects.get(
            id=self.context["view"].kwargs.get("supplier_id")
        )
        for service_data in booking_services_data:
            service = Service.objects.filter(
                supplier=supplier,
                **dict(service_data),
            ).first()
            try:
                specialist_type = service.specialist_type
                service_data.update(
                    {
                        "supplier_id": self.context["view"].kwargs.get(
                            "supplier_id"
                        ),
                        "specialist_type": specialist_type,
                    }
                )
                Service.objects.filter(**service_data).update(
                    booking=booking_service
                )
            except AttributeError:
                raise serializers.ValidationError(
                    {"error": "У специалиста нет такой услуги!"}
                )
        return booking_service

    def validate(self, data):
        _data = deepcopy(data)
        service = _data.get("booking_services")
        for service_data in service:
            pet_data = _data.pop("pet")
            age = Age.objects.get_or_create(**pet_data.pop("age"))
            pet_data.update(
                {
                    "age": age[0],
                    "owner": CustomerProfile.objects.get(
                        related_user=self.context.get("request").user
                    ),
                }
            )
            if Pet.objects.filter(**pet_data).exists():
                pet_id = Pet.objects.filter(**pet_data).first().id
            else:
                pet_id = None
            if Booking.objects.filter(
                booking_services__name=service_data.get("name"),
                booking_services__price=service_data.get("price"),
                booking_services__pet_type=service_data.get("pet_type"),
                customer=self.context.get("request").user.profile_id,
                supplier=self.context.get("view").kwargs.get("supplier_id"),
                pet=pet_id,
            ).exists():
                raise serializers.ValidationError(
                    "Такая бронь уже существует!"
                )
        return data

    class Meta(BaseBookingSerializer.Meta):
        fields = BaseBookingSerializer.Meta.fields + (
            "id",
            "booking_services",
        )


class BookingServiceRetrieveSerializer(BaseBookingSerializer):
    service = ServiceSerializer(
        read_only=True,
    )
