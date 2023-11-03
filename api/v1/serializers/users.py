from rest_framework import serializers

from api.v1.serializers.core import (
    Base64ImageField,
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
            "phone_number",
            "last_name",
            "first_name",
            "user",
        ]
    # def to_internal_value(self, data):
    #     password = data.pop("password", None)
    #     email = data.pop("email", None)
    #     data["user"] = {
    #         "email": email,
    #         "password": password,
    #     }
    #     return data
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
    pass


class SupplierProfileSerializer(BaseProfileSerializer):

    class Meta:
        model = SupplierProfile
        fields = BaseProfileSerializer.Meta.fields + [
            "photo",
        ]


class CustomerPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = [
        "id",
        "phone_number",
        "last_name",
        "first_name",
        "photo",
    ]

class CustomerSerializer(CustomerPatchSerializer):
    def to_internal_value(self, data):
        return super().to_internal_value(data)

    pet = PetSerializer(
        many=True,
        read_only=True,
    )

    class Meta(CustomerPatchSerializer.Meta):
        fields = CustomerPatchSerializer.Meta.fields + [
            "pet", "photo",
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
