from icecream import ic
from rest_framework import serializers

from api.v1.serializers.core import (
    Base64ImageField,
    ScheduleSerializer,
    PriceSerializer,
)
from api.v1.serializers.pets import PetSerializer
from services.models import Booking
from users.models import CustomerProfile, SupplierProfile, User


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}


class BaseProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    photo = Base64ImageField(
        allow_null=True,
        required=False,
    )

    class Meta:
        model = CustomerProfile
        fields = [
            "id",
            "photo",
            "phone_number",
            "contact_email",
            "user",
        ]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        profile = self.Meta.model.objects.create(**validated_data)
        User.objects.create_user(**user_data, profile=profile)
        return profile


class CustomerProfileSerializer(BaseProfileSerializer):
    pass


class SupplierProfileSerializer(BaseProfileSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_representation = representation.pop("user")
        for key in user_representation:
            representation[key] = user_representation[key]
        return representation

    class Meta:
        model = SupplierProfile
        fields = (
            "photo",
            "phone_number",
            "contact_email",
            "user",
        )


class SupplierSerializer(BaseProfileSerializer):
    class Meta:
        model = SupplierProfile
        verbose_name = "специалист"
        verbose_name_plural = "специалисты"
        fields = [
            "phone_number",
            "contact_email",
            "address",
            "photo",
        ]


class CustomerPatchSerializer(BaseProfileSerializer):
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     user_representation = representation.pop("user")
    #     for key in user_representation:
    #         representation[key] = user_representation[key]
    #     return representation
    # def to_internal_value(self, data):
    #     password = data.pop("password", None)
    #     email = data.pop("email", None)
    #     data["user"] = {
    #         "email": email,
    #         "password": password,
    #     }
    #     data = super().to_internal_value(data)
    #     return data

    def get_field_names(self, declared_fields, info):
        fields = super().get_field_names(declared_fields, info)
        if "user" in fields:
            fields.remove("user")
        fields.extend(["first_name", "last_name"])
        return fields


class CustomerSerializer(CustomerPatchSerializer):
    pet = PetSerializer(
        many=True,
        read_only=True,
    )

    class Meta(CustomerPatchSerializer.Meta):
        fields = CustomerPatchSerializer.Meta.fields + [
            "pet",
        ]


class BookingListSerializer(serializers.ModelSerializer):
    price = PriceSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            "description",
            "price",
            "to_date",
            "customer",
            "is_done",
        ]
