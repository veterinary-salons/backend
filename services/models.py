from django.db.models import UniqueConstraint, CheckConstraint, Q, F
from django.utils import timezone

from core.constants import Limits, Default
from django.contrib.auth import get_user_model
from django.db import models

from core.validators import (
    validate_alphanumeric,
    RangeValueValidator,
    validate_current_and_future_month,
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

    customer_place = models.BooleanField(
        default=False,
    )
    supplier_place = models.BooleanField(
        default=True,
    )
    cost_from = models.DecimalField(
        decimal_places=0,
        max_digits=5,
        default=Default.COST_FROM,
        validators=[RangeValueValidator(Limits.MIN_PRICE, Limits.MAX_PRICE)],
    )
    cost_to = models.DecimalField(
        decimal_places=0,
        max_digits=5,
        default = Default.COST_TO,
        validators=[RangeValueValidator(Limits.MIN_PRICE, Limits.MAX_PRICE)],
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
            CheckConstraint(
                check=Q(cost_from__lte=F("cost_to")),
                name="cost_range",
            ),
        )

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

    class Meta:
        verbose_name = "бронь услуги"
        verbose_name_plural = "брони услуг"

    def __str__(self):
        return f"{self.service.name} - {self.date}"
