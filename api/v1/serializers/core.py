import base64
from uuid import uuid4

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from core.models import Schedule, Price
from services.models import Service


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
            "weekday",
            "is_working_day",
            "start_work_time",
            "end_work_time",
            "break_start_time",
            "break_end_time",
            "service",
        )

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = (
            "service_name",
            "cost_from",
        )
