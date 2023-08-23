from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator

from .validators import phone_number_validator


class User(AbstractUser):
    email = models.EmailField(
        unique=True, max_length=50, validators=[MinLengthValidator(5)]
    )
    first_name = models.CharField(
        max_length=15,  validators=[MinLengthValidator(2)]
    )
    last_name = models.CharField(
        max_length=15, validators=[MinLengthValidator(2)]
    )
    phone_number = models.CharField(
        max_length=12, 
        validators=[MinLengthValidator(10), phone_number_validator]
    )
    address = models.CharField(max_length=100)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number", "address"]

    @property
    def customer_profile(self):
        if hasattr(self, "related_customer"):
            return self.customer_related
        return None

    @property
    def supplier_profile(self):
        if hasattr(self, "related_supplier"):
            return self.supplier_related
        return None

class CustomerProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="related_customer"
    )

class SupplierProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="related_supplier"
    )
    photo = models.ImageField(blank=True, null=True)
