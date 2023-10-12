import base64
from uuid import uuid4

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import serializers

from users.models import CustomerProfile, SupplierProfile, User


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
            "first_name",
            "last_name",
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
        fields = "__all__"

class SupplierProfileSerializer(BaseProfileSerializer):
    class Meta:
        model = SupplierProfile
        fields = "__all__"


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

class CustomerSerializer(CustomerProfileSerializer):

    class Meta:
        model = CustomerProfile
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        fields = (
            "phone_number",
            "contact_email",
            "address",
            "user",
        )
