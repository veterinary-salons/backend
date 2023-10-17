from hashlib import md5 as md5_hash

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.v1.serializers.core import Base64ImageField
from authentication.tokens import RecoveryAccessToken
from authentication.utils import get_recovery_code
from core.constants import Limits

from users.models import CustomerProfile, SupplierProfile

User = get_user_model()


class SignUpProfileSerializer(serializers.Serializer):
    profile_type = serializers.ChoiceField(
        choices=("customer", "supplier")
    )
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()
    email = serializers.EmailField(max_length=Limits.MAX_LEN_EMAIL)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user_data = {
            field: attrs.pop(field)
            for field in {"first_name", "last_name", "email", "password"}
        }
        attrs["user"] = user_data
        return attrs

    def create(self, validated_data):
        profile_type = validated_data.pop("profile_type")
        user_data = validated_data.pop("user")
        if profile_type == "customer":
            profile = CustomerProfile.objects.create(**validated_data)
            user = User.objects.create_user(**user_data, profile=profile)


class RecoveryEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=Limits.MAX_LEN_EMAIL,
        write_only=True,
    )
    token = serializers.CharField(read_only=True)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "a user with this email does not exist"
            )
        return value

    def validate(self, attrs):
        email = attrs.get("email")
        user = User.objects.get(email=email)
        token = RecoveryAccessToken.for_user(user)
        attrs["token"] = str(token)
        code = get_recovery_code(email)
        if not code.is_valid:
            code.update_code()
        attrs["code"] = code.code
        return attrs

class RecoveryCodeSerializer(serializers.Serializer):
    code = serializers.CharField(
        min_length=Limits.CONFIRMATION_CODE_LENGTH, 
        max_length=Limits.CONFIRMATION_CODE_LENGTH,
        write_only=True,
    )

    def validate_code(self, value):
        email = self.context["request"].user.email
        recovery_code = get_recovery_code(email)
        if not recovery_code.is_valid:
            recovery_code.update_code()
            raise serializers.ValidationError("code is expired")
        if value != recovery_code.code:
            raise serializers.ValidationError("incorrect code")
        recovery_code.confirm()
        return value

class RecoveryPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = self.context["request"].user
        password = validated_data.get("password")
        user.set_password(password)
        user.save()
        return user

class BasicProfileInfoSerializer(serializers.Serializer):
    profile_type = serializers.ChoiceField(
        choices=("customer", "supplier")
    )
    id = serializers.IntegerField()
    email = serializers.EmailField(
        max_length=Limits.MAX_LEN_EMAIL,
    )
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()
    image = Base64ImageField(
        required=False, allow_null=True,
    )


class SignInSerializer(TokenObtainPairSerializer):
    profile_data_serializer_class = BasicProfileInfoSerializer

    def validate(self, attrs):
        token_data = super().validate(attrs)
        profile = self.user.profile
        if not profile:
            raise serializers.ValidationError("this profile does not exist")
        if isinstance(profile, SupplierProfile):
            profile_type = "supplier"
            image = profile.photo
        else:
            profile_type = "customer"
            image = None
        profile_fields = {
            "profile_type": profile_type,
            "id": self.user.id,
            "email": self.user.email,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "phone_number": profile.phone_number,
            "image": image
        }
        profile_serializer = self.profile_data_serializer_class(
            instance=profile_fields
        )
        profile_data = profile_serializer.data
        return {
            "token_data": token_data,
            "profile_data": profile_data,
        }
