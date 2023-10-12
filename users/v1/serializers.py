from hashlib import md5 as md5_hash

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from authentication.tokens import RecoveryAccessToken
from users.models import CustomerProfile, SupplierProfile, User
from core.constants import Limits
from core.serializers import Base64ImageField


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
    photo = Base64ImageField(
        allow_null=True,
        required=False,
    )

    class Meta:
        model = SupplierProfile
        fields = "__all__"


class SupplierSerializer(BaseProfileSerializer):
    photo = Base64ImageField(allow_null=True)

    class Meta:
        model = SupplierProfile
        verbose_name = "Специалист"
        verbose_name_plural = "Специалисты"
        fields = (
            "phone_number",
            "contact_email",
            "address",
            "photo",
        )