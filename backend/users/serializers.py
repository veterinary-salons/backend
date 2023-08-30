import base64
from uuid import uuid4

from django.contrib.auth import authenticate
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import serializers

from users.models import User, CustomerProfile, SupplierProfile


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        header, encoded_data = data.split(";base64,")
        decoded_data = base64.b64decode(encoded_data)
        image_extension = header.split("/")[1]
        file_name = f"{uuid4()}.{image_extension}"
        return super().to_internal_value(
            SimpleUploadedFile(
                name=file_name,
                content=decoded_data
            )
        )

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")

class BaseProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        profile = self.Meta.model.objects.create(**validated_data)
        user = User.objects.create(**user_data, profile=profile)
        return profile

class CustomerProfileSerializer(BaseProfileSerializer):

    class Meta:
        model = CustomerProfile
        fields = "__all__"

class SupplierProfileSerializer(BaseProfileSerializer):
    photo = Base64ImageField()

    class Meta:
        model = SupplierProfile
        fields = "__all__"