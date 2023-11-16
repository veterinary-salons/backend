from django.urls import reverse
from drf_extra_fields.fields import Base64ImageField
from icecream import ic
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from backend.settings import MEDIA_URL
from core.constants import Default
from core.models import Schedule, Slot
from core.validators import validate_price, validate_schedule
from services.models import Price


class Base64ImageFieldPath(Base64ImageField):
    def get_path(self, file) -> str:
        request = self.context.get("request")
        domain = request.META.get("HTTP_HOST")
        profile_type = self.context.get("request").data.get("profile_type")

        if profile_type == "customer":
            path = Default.PATH_TO_AVATAR_CUSTOMER
        elif profile_type == "supplier":
            path = Default.PATH_TO_AVATAR_SUPPLIER
        else:
            raise serializers.ValidationError(
                "Неправильный тип профиля, только `customer` или `supplier`"
            )
        url = (
            f"{Default.PROTOCOL}{domain}"
            + MEDIA_URL
            + path
            + file.name
        )
        return url

    def to_representation(self, value):
        if not value:
            return None

        return self.get_path(value)


class ScheduleSerializer(serializers.ModelSerializer):
    service = PrimaryKeyRelatedField(
        read_only=True,
    )

    def to_internal_value(self, data):
        time_per_visit = data.pop("time_per_visit", None)
        if time_per_visit:
            data["time_per_visit"] = int(float(time_per_visit) * 60)
        return super().to_internal_value(data)

    class Meta:
        model = Schedule
        fields = (
            "id",
            "weekday",
            "is_working_day",
            "start_work_time",
            "end_work_time",
            "break_start_time",
            "break_end_time",
            "time_per_visit",
            "service",
        )

    def validate(self, attrs):
        validate_schedule(attrs)
        return attrs


class PriceSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        validate_price(attrs)
        return attrs

    class Meta:
        model = Price
        fields = (
            "service_name",
            "cost_from",
            "cost_to",
        )


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = (
            "id",
            "date",
            "time",
        )
