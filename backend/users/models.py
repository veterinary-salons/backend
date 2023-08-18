from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.contenttypes.fields import (
    GenericForeignKey, GenericRelation
)
from django.contrib.contenttypes.models import ContentType


class User(AbstractBaseUser):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    content_type = models.OneToOneField(
        ContentType, null=True, on_delete=models.SET_NULL
    )
    profile_id = models.PositiveIntegerField(blank=True, null=True)
    profile = GenericForeignKey("content_type", "profile_id")

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    @property
    def is_customer(self):
        return isinstance(self.profile, CustomerProfile)

    @property
    def is_supplier(self):
        return isinstance(self.profile, SupplierProfile)

class Profile(models.Model):
    user = GenericRelation(User)
    photo = models.ImageField()

    class Meta:
        abstract = True

class CustomerProfile(Profile):
    pass

class SupplierProfile(Profile):
    pass
