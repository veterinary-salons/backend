import base64
from datetime import timedelta
from uuid import uuid4

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.backends.utils import format_number
from icecream import ic
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField
from decimal import Decimal

from core.models import Schedule
from core.validators import validate_price, validate_schedule
from services.models import Price


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        header, encoded_data = data.split(";base64,")
        decoded_data = base64.b64decode(encoded_data)
        image_extension = header.split("/")[1]
        file_name = f"{uuid4()}.{image_extension}"
        return super().to_internal_value(
            SimpleUploadedFile(
                name=file_name,
                content=decoded_data,
            ),
        )

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
