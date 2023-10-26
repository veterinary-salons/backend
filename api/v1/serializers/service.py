from copy import deepcopy

from icecream import ic

from api.v1.serializers.core import (
    ScheduleSerializer,
    PriceSerializer,
    Base64ImageField,
)
from api.v1.serializers.pets import BasePetSerializer
from api.v1.serializers.users import (
    SupplierProfileSerializer,
)
from core.constants import Limits, Default
from core.models import Schedule, Price
from core.utils import (
    update_schedules,
    create_schedules,
    delete_schedules,
    update_prices,
    create_prices,
    delete_prices,
)

from pets.models import Pet, Age
from services.models import Booking
from users.models import SupplierProfile, CustomerProfile

from rest_framework import serializers
from services.models import Service

class BaseServiceSerializer(serializers.ModelSerializer):
    """Сериализация базовой модели услуг."""
    schedules = ScheduleSerializer(many=True)
    price = PriceSerializer(many=True, source="prices")
    image = Base64ImageField(required=False, allow_null=True)
    class Meta:
        model = Service
        fields = (
            "category",
            "ad_title",
            "description",
            "price",
            "image",
            "extra_fields",
            "customer_place",
            "supplier_place",
            "schedules",
        )
class ServiceCreateSerializer(BaseServiceSerializer):
    """Сериализация всех услуг."""
    def create(self, validated_data):
        schedules_data = validated_data.pop("schedules", [])
        prices_data = validated_data.pop("prices", [])
        service = super().create(validated_data)
        schedules = []
        prices = []
        for schedule_data in schedules_data:
            schedule = Schedule(service=service, **schedule_data)
            schedule.clean()
            schedules.append(schedule)
        for price_data in prices_data:
            price = Price(service=service, **price_data)
            price.clean()
            prices.append(price)
        Schedule.objects.bulk_create(schedules)
        Price.objects.bulk_create(prices)
        return service

class ServiceUpdateSerializer(BaseServiceSerializer):
    """Сериализация всех услуг."""

    def update(self, instance, validated_data):
        schedules_data = validated_data.pop("schedules", [])
        prices_data = validated_data.pop("prices", [])
        instance = super().update(instance, validated_data)
        schedules = instance.schedules.all()
        prices = instance.prices.all()

        update_schedules(schedules, schedules_data)
        create_schedules(instance, schedules_data)
        delete_schedules(instance, schedules, schedules_data)

        update_prices( prices, prices_data)
        create_prices(instance, prices_data)
        delete_prices(instance, prices, prices_data)

        return instance

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
    """Базовый сериализатор бронирования."""

    supplier = SupplierProfileSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = (
            "to_date",
            "pet",
        )


class BookingSerializer(BaseBookingSerializer):
    """Сериализатор бронирования."""

    booking_services = ServiceCreateSerializer(
        many=True,
    )
    pet = BasePetSerializer()

    def create(self, validated_data, **kwargs):
        """Создание бронирования.

        Обрабатываем вложенные поля `service` и `pet` и вложенное
        в `pet` `age`.

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
