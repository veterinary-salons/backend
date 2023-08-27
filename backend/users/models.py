from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import (
    GenericForeignKey, GenericRelation
)
from django.core.validators import MinLengthValidator

from .validators import phone_number_validator


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
        # checks from django UserManager source code
        # in case we'll ever change `is_superuser` or `is_staff` default values
        if extra_fields.setdefault("is_staff", True) is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.setdefault("is_superuser", True) is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = models.NOT_PROVIDED
    email = models.EmailField(
        unique=True, max_length=50, validators=[MinLengthValidator(5)]
    )
    first_name = models.CharField(
        max_length=15, validators=[MinLengthValidator(2)]
    )
    last_name = models.CharField(
        max_length=15, validators=[MinLengthValidator(2)]
    )

    profile_content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, blank=True, null=True
    )
    profile_id = models.PositiveIntegerField(blank=True, null=True)
    profile = GenericForeignKey(
        "profile_content_type", "profile_id"
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        indexes = [
            models.Index(fields=["profile_content_type", "profile_id"]),
        ]


class BaseProfile(models.Model):
    related_user = GenericRelation(
        User,
        content_type_field="profile_content_type",
        object_id_field="profile_id"
    )

    phone_number = models.CharField(
        max_length=12, 
        validators=[MinLengthValidator(10), phone_number_validator]
    )
    address = models.CharField(max_length=100)

    @property
    def user(self):
        return self.related_user.first()

    class Meta:
        abstract = True

class CustomerProfile(BaseProfile):
    pass


class SupplierProfile(BaseProfile):
    photo = models.ImageField(blank=True, null=True)
