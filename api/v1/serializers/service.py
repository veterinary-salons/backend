from rest_framework.relations import PrimaryKeyRelatedField

from api.v1.serializers.core import (
    ScheduleSerializer,
    PriceSerializer,
    Base64ImageField,
)
from api.v1.serializers.users import (
    SupplierProfileSerializer,
)
from core.constants import Limits, Default
from core.models import Schedule
from core.utils import (
    update_schedules,
    create_schedules,
    delete_schedules,
    update_prices,
    create_prices,
    delete_prices,
)

from services.models import Booking, Price, Review

from rest_framework import serializers
from services.models import Service


class SmallServiceSerializer(serializers.ModelSerializer):
    """Сериализация услуг с минимальными данными."""
    class Meta:
        model = Service
        fields = (
            "id",
            "category",
        )

class BaseServiceSerializer(serializers.ModelSerializer):
    """Сериализация базовой модели услуг."""

    schedules = ScheduleSerializer(many=True)
    price = PriceSerializer(many=True, source="prices")
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Service
        fields = (
            "id",
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

        update_prices(prices, prices_data)
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


class BookingSerializer(serializers.ModelSerializer):
    """Сериализатор бронирования."""

    class Meta:
        model = Booking
        fields = [
            "description",
            "price",
            "to_date",
            "is_confirmed",
            "is_done",
        ]

#
class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""
    review = serializers.CharField(source="text")
    class Meta:
        model = Review
        fields = (
            "review",
            "rating",
        )
