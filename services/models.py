from django.db.models import UniqueConstraint
from django.utils import timezone

from core.constants import Default, Limits
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models

from core.models import Schedule
from core.utils import default_price
from core.validators import (
    validate_alphanumeric,
    RangeValueValidator,
    validate_current_and_future_month,
    validate_services,
)
from pets.models import Pet
from users.models import SupplierProfile, CustomerProfile

User = get_user_model()

class BaseService(models.Model):
    """Базовая модель для услуг."""

    name = models.CharField(
        verbose_name="название услуги",
        max_length=Limits.MAX_LEN_SERVICE_NAME,
        null=False,
        blank=False,
        validators=(validate_alphanumeric,),
    )
    supplier = models.ForeignKey(
        SupplierProfile,
        on_delete=models.CASCADE,
    )
    class Meta:
        abstract = True

class Service(BaseService):
    """Модель услуг."""

    pet_type = models.CharField(
        verbose_name="тип животного",
        max_length=Limits.MAX_LEN_ANIMAL_TYPE,
        choices=Default.PET_TYPE,
    )
    schedule = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, null=True, blank=True
    )
    price = ArrayField(
        models.PositiveIntegerField(
            validators=[
                RangeValueValidator(Limits.MIN_PRICE, Limits.MAX_PRICE)
            ]
        ),
        null=False,
        blank=False,
        default=default_price,
    )
    description = models.TextField(
        max_length=Limits.MAX_LEN_ABOUT,
        verbose_name="О себе",
        blank=True,
        null=True,
        validators=(validate_alphanumeric,),
    )
    published = models.BooleanField(
        default=False,
    )
    class Meta:
        verbose_name = "услуга"
        verbose_name_plural = "услуги"
        constraints = (
            UniqueConstraint(
                fields=(
                    "name",
                    "supplier",
                ),
                name="unique_for_services",
            ),
        )

    def clean(self):
        """Проверяем соответствие типа специалиста и типа питомца."""

        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Service, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Booking(BaseService):
    """Модель бронирования услуги."""

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="booking_services",
    )
    date = models.DateTimeField(auto_now_add=True)
    to_date = models.DateTimeField(
        validators=(validate_current_and_future_month,),
        blank=False,
        null=False,
        default=timezone.now,
    )
    place = models.CharField(
        max_length=Limits.MAX_PLACE_LENGTH,
        blank=True,
        null=True,
        validators=(validate_alphanumeric,),
    )
    customer = models.ForeignKey(
        CustomerProfile,
        models.CASCADE,
        null=False,
        blank=False,
    )
    is_done = models.BooleanField(
        verbose_name="подтверждено или нет",
        default=False,
    )
    actual = models.BooleanField(
        verbose_name="активно или нет",
        default=False,
    )
    customer_place = models.BooleanField(default=False,)
    supplier_place = models.BooleanField(default=True,)

    class Meta:
        verbose_name = "бронь услуги"
        verbose_name_plural = "брони услуг"

    def __str__(self):
        return f"{self.service.name} - {self.date}"

