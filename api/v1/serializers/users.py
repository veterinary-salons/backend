from django.contrib.auth.password_validation import validate_password
from drf_extra_fields.fields import Base64ImageField
from icecream import ic

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.v1.serializers.core import (
    Base64ImageField,
    PriceSerializer,
    Base64ImageFieldUser,
)
from api.v1.serializers.pets import PetSerializer
from services.models import Booking
from users.models import CustomerProfile, SupplierProfile, User


class CustomUserSerializer(serializers.ModelSerializer):
    @staticmethod
    def check_password(value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value

    class Meta:
        model = User
        fields = (
            "email",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}


class BaseProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = CustomerProfile
        fields = [
            "id",
            "phone_number",
            "last_name",
            "first_name",
            "user",
            "image",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_representation = representation.pop("user")
        for key in user_representation:
            representation[key] = user_representation[key]
        return representation

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        profile = self.Meta.model.objects.create(**validated_data)
        User.objects.create_user(**user_data, profile=profile)
        return profile


class CustomerProfileSerializer(BaseProfileSerializer):
    image = Base64ImageFieldUser(
        allow_empty_file=True,
        required=False,
    )


class SupplierProfileSerializer(BaseProfileSerializer):
    image = Base64ImageFieldUser(
        allow_empty_file=True,
        required=False,
    )

    class Meta:
        model = SupplierProfile
        fields = BaseProfileSerializer.Meta.fields + [
            "address",
        ]


class CustomerPatchSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
        allow_empty_file=True,
        required=False,
    )

    class Meta:
        model = CustomerProfile
        fields = [
            "id",
            "phone_number",
            "last_name",
            "first_name",
            "image",
            "address",
        ]


class CustomerSerializer(CustomerPatchSerializer):
    image = Base64ImageField(
        allow_empty_file=True,
        required=False,
    )
    pet = PetSerializer(
        many=True,
        read_only=True,
    )

    class Meta(CustomerPatchSerializer.Meta):
        fields = CustomerPatchSerializer.Meta.fields + [
            "pet",
            "image",
        ]


class BookingListSerializer(serializers.ModelSerializer):
    price = PriceSerializer(read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["supplier"] = SupplierProfileSerializer(
            instance.price.service.supplier
        ).data
        return representation

    class Meta:
        model = Booking
        fields = [
            "description",
            "price",
            "to_date",
            "is_done",
        ]
