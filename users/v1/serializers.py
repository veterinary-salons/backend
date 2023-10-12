import base64
from hashlib import md5 as md5_hash
from uuid import uuid4

from django.core.files.uploadedfile import SimpleUploadedFile
from icecream import ic
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from pets.models import Pet
from pets.serializers import PetSerializer
from authentication.tokens import RecoveryAccessToken
from users.models import CustomerProfile, SupplierProfile, User
from core.constants import Limits


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

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        profile = self.Meta.model.objects.create(**validated_data)
        User.objects.create_user(**user_data, profile=profile)
        return profile


class CustomerProfileSerializer(BaseProfileSerializer):
    class Meta:
        model = CustomerProfile
        fields = (
            "id",
            "photo",
            "phone_number",
            "contact_email",
            "user",
        )


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
        fields = (
            "phone_number",
            "contact_email",
            "address",
            "photo",
        )

class CustomerPatchSerializer(BaseProfileSerializer):

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_representation = representation.pop("user")
        for key in user_representation:
            representation[key] = user_representation[key]
        return representation

    class Meta(CustomerProfileSerializer.Meta):
        fields = CustomerProfileSerializer.Meta.fields + (
            "first_name",
            "last_name",
        )
class CustomerSerializer(CustomerPatchSerializer):
    pet = PetSerializer(
        many=True, read_only=True,
    )
    class Meta(CustomerPatchSerializer.Meta):
        fields = CustomerPatchSerializer.Meta.fields + ("pet",)
