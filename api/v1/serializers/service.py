from django.db.models import Q
from drf_extra_fields.fields import Base64ImageField
from icecream import ic
from rest_framework.relations import PrimaryKeyRelatedField

from api.v1.serializers.core import (
    ScheduleSerializer,
    PriceSerializer,
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
    get_customer,
)

from services.models import Booking, Price, Review, Favorite, FavoriteArticles

from rest_framework import serializers
from services.models import Service
from users.models import CustomerProfile


class SmallServiceSerializer(serializers.ModelSerializer):
    """Сериализация услуг с минимальными данными."""

    class Meta:
        model = Service
        fields = (
            "id",
            "ad_title",
            "category",
            "description",
        )


class BaseServiceSerializer(serializers.ModelSerializer):
    """Сериализация базовой модели услуг."""

    schedules = ScheduleSerializer(many=True)
    price = PriceSerializer(many=True, source="prices")

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

    image = Base64ImageField(
        allow_empty_file=True,
        required=False,
    )

    def create(self, validated_data):
        schedules_data = validated_data.pop("schedules", [])
        prices_data = validated_data.pop("prices", [])
        service = super().create(validated_data)
        schedules = []
        prices = []
        for schedule_data in schedules_data:
            schedule = Schedule(service_id=service.id, **schedule_data)
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
    """Сериализация обновления всех услуг."""

    image = Base64ImageField(
        allow_empty_file=True,
        required=False,
    )

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


class BookingSerializer(serializers.ModelSerializer):
    """Сериализатор бронирования."""

    def validate(self, attrs):
        to_date = attrs.get("to_date")
        price_id = attrs.get("price")
        weekday = Default.DAYS_NUMBER.get(to_date.weekday())
        try:
            schedule = Schedule.objects.get(
                Q(service__prices=price_id) & Q(weekday=weekday)
            )
        except Schedule.DoesNotExist:
            raise serializers.ValidationError(
                "Невозможно забронировать услугу. У исполнителя нет "
                "расписания на эту дату.."
            )
        time_from = schedule.start_work_time
        time_to = schedule.end_work_time
        if time_from > to_date.time() or to_date.time() > time_to:
            raise serializers.ValidationError(
                "Невозможно забронировать услугу. Это время занято."
            )
        return attrs

    class Meta:
        model = Booking
        fields = [
            "description",
            "price",
            "to_date",
            "is_confirmed",
            "is_done",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов."""

    review = serializers.CharField(source="text")

    class Meta:
        model = Review
        fields = (
            "review",
            "rating",
        )


class FavoriteSerializer(serializers.ModelSerializer):
    service = PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
    )
    """Сериализатор избранного."""

    def validate(self, attrs):
        customer = get_customer(self.context.get("request"), CustomerProfile)
        service = attrs.get("service")
        services = Service.objects.filter(in_favorites__customer=customer)
        if service in services:
            raise serializers.ValidationError(
                "Эта услуга у вас уже добавлена в избранное."
            )
        return attrs

    class Meta:
        model = Favorite
        fields = [
            "id",
            "service",
            "date_added",
        ]


class FavoriteArticlesSerializer(serializers.ModelSerializer):
    """Сериализатор избранного."""

    def validate(self, attrs):
        customer = get_customer(self.context.get("request"), CustomerProfile)
        article_id = attrs.get("article_id")
        articles = [
            favorite.article_id
            for favorite in FavoriteArticles.objects.filter(customer=customer)
        ]
        if article_id in articles:
            raise serializers.ValidationError(
                "Эта статья у вас уже добавлена в избранное."
            )
        return attrs

    class Meta:
        model = FavoriteArticles
        fields = (
            "article_id",
            "date_added",
        )
