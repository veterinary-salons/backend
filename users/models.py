from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import (
    GenericForeignKey,
    GenericRelation,
)
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinLengthValidator
from django.db import models
from rest_framework import serializers

from core.constants import Limits, Default
from core.validators import (
    PhoneNumberValidator,
    validate_letters,
    validate_alphanumeric,
)
from users.validators import phone_number_validator


class CustomUserManager(BaseUserManager):
    """
    The implementation here is almost the same as in
    django.contrib.auth.models.UserManager because we only need to customize
    creation of users with email as username and keep the good practice
    of using the _create_user method.
    """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        if extra_fields.setdefault("is_staff", True) is False:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.setdefault("is_superuser", True) is False:
            raise ValueError("Superuser must have is_superuser=True")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.NOT_PROVIDED
    first_name = None
    last_name = None
    email = models.EmailField(
        unique=True,
        max_length=Limits.MAX_LEN_EMAIL,
    )
    profile_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    profile_id = models.PositiveIntegerField(blank=True, null=True)
    profile = GenericForeignKey("profile_content_type", "profile_id")

    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        indexes = [
            models.Index(
                fields=[
                    "profile_content_type",
                    "profile_id",
                ]
            ),
        ]


class BaseProfile(models.Model):
    related_user = GenericRelation(
        User,
        content_type_field="profile_content_type",
        object_id_field="profile_id",
    )
    first_name = models.CharField(
        max_length=15,
        validators=[
            MinLengthValidator(2),
        ],
    )
    last_name = models.CharField(
        max_length=15,
        validators=[
            MinLengthValidator(2),
        ],
    )
    phone_number = models.CharField(
        max_length=12,
        validators=[
            PhoneNumberValidator(
                Limits.MIN_LEN_PHONE_NUMBER, Limits.MAX_LEN_PHONE_NUMBER
            ),
            phone_number_validator,
        ],
    )
    address = models.CharField(
        max_length=Limits.MAX_LEN_ADDRESS,
        blank=True,
        null=True,
    )
    photo = models.ImageField(blank=True, null=True)
    contact_email = models.EmailField(
        max_length=Limits.MAX_LEN_EMAIL, null=True, blank=True
    )

    @property
    def user(self):
        return self.related_user.first()

    class Meta:
        abstract = True


class SupplierProfile(BaseProfile):
    specialist_type = models.CharField(
        verbose_name="тип услуги",
        max_length=Limits.MAX_LEN_SERVICE_TYPE,
        choices=Default.SERVICES,
        validators=(validate_letters,),
        blank=False,
        null=False,
    )
    pet_type = models.CharField(
        verbose_name="тип животного",
        max_length=Limits.MAX_LEN_ANIMAL_TYPE,
        choices=Default.PET_TYPE,
    )
    about = models.TextField(
        max_length=Limits.MAX_LEN_ABOUT,
        verbose_name="О себе",
        blank=True,
        null=True,
        validators=(validate_alphanumeric,),
    )

    def clean(self):
        """Проверяем соответствие типа специалиста и типа питомца."""
        if (
            self.specialist_type == Default.SERVICES[1][0]
            and self.pet_type != Default.PET_TYPE[1][0]
        ):
            raise serializers.ValidationError(
                "Кинолог работает только с собаками."
            )
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(SupplierProfile, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email}"


class CustomerProfile(BaseProfile):

    def __str__(self):
        return f"{self.phone_number}"
