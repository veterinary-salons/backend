from django.db.models import UniqueConstraint, CheckConstraint, Q, F, JSONField
from django.utils import timezone
from icecream import ic
from rest_framework import serializers

from core.constants import Limits, Default, Messages
from django.contrib.auth import get_user_model
from django.db import models

from core.validators import (
    validate_alphanumeric,
    validate_current_and_future_month,
    validate_cynology_service,
    validate_cynology_fields,
    validate_vet_service,
    validate_vet_fields,
    validate_grooming_service,
    validate_grooming_fields,
    validate_shelter_service,
    validate_shelter_fields,
    validate_letters,
    validate_pet_type,
)
from pets.models import Pet
from users.models import SupplierProfile, CustomerProfile

User = get_user_model()


class BaseService(models.Model):
    """Базовая модель для услуг."""

    ad_title = models.CharField(
        max_length=Limits.MAX_LEN_TITLE_NAME,
        null=False,
        blank=False,
        validators=[validate_alphanumeric],
    )

    class Meta:
        abstract = True


class Service(BaseService):
    """Модель услуг."""
    category = models.CharField(
        verbose_name="тип услуги",
        max_length=Limits.MAX_LEN_SERVICE_TYPE,
        choices=Default.SERVICES,
        validators=(validate_letters,),
        blank=False,
        null=False,
    )
    description = models.CharField(
        max_length=Limits.MAX_LEN_SERVICE_NAME,
        null=False,
        blank=False,
    )
    supplier = models.ForeignKey(
        SupplierProfile,
        on_delete=models.CASCADE,
        related_name="services",
        verbose_name="исполнитель",
        null=False,
        blank=False,
    )
    customer_place = models.BooleanField(
        default=False,
    )
    supplier_place = models.BooleanField(
        default=True,
    )
    image = models.ImageField(
        upload_to="images",
        blank=True,
        null=True,
    )
    extra_fields = JSONField()

    class Meta:
        verbose_name = "услуга"
        verbose_name_plural = "услуги"
        constraints = (
            # UniqueConstraint(
            #     fields=["name", "supplier"],
            #     name="unique_name_for_service",
            # )
        )

    def clean(self):
        """Проверяем соответствие типа специалиста и типа питомца."""
        specialist_type = self.category
        service_name = self.extra_fields.get("service_name")
    
        if specialist_type == Default.SERVICES[0][0]:
            validate_cynology_service(service_name)
            validate_cynology_fields(self)
        elif specialist_type == Default.SERVICES[1][0]:
            validate_vet_service(service_name)
            validate_vet_fields(self)
        elif specialist_type == Default.SERVICES[2][0]:
            validate_grooming_service(service_name)
            validate_grooming_fields(self)
        elif specialist_type == Default.SERVICES[3][0]:
            validate_shelter_service(service_name)
            validate_shelter_fields(self)
        validate_pet_type(self)

        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Service, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.extra_fields.get('service_name')} - {self.ad_title}"


class Booking(BaseService):
    """Модель бронирования услуги."""

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="bookingservices",
    )
    customer = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="пользователь",
        blank=False,
        null=False,
    )
    supplier = models.ForeignKey(
        SupplierProfile,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="исполнитель",
        blank=False,
        null=False,
    )
    date = models.DateTimeField(auto_now_add=True)
    to_date = models.DateTimeField(
        validators=(validate_current_and_future_month,),
        blank=False,
        null=False,
        default=timezone.now,
    )
    is_confirmed = models.BooleanField(
        verbose_name="подтверждено или нет",
        default=False,
    )
    is_done = models.BooleanField(
        verbose_name="исполнено или нет",
        default=False,
    )

    class Meta:
        verbose_name = "бронь услуги"
        verbose_name_plural = "брони услуг"
        constraints = (
            UniqueConstraint(
                fields=(
                    "service",
                    "supplier",
                ),
                name="unique_for_services",
            ),
            UniqueConstraint(
                fields=(
                    "service",
                    "supplier",
                ),
                name="unique_for_booking",
            ),
        )

    def __str__(self):
        return f"{self.service.name} - {self.date}"



# class Advertisement(BaseService):
#     """Модель объявления услуги."""
#
#     supplier = models.ForeignKey(
#         SupplierProfile,
#         on_delete=models.CASCADE,
#         null=False,
#         blank=False,
#         related_name="advertisements",
#     )
#     service = models.ForeignKey(
#         Service,
#         on_delete=models.CASCADE,
#         related_name="advertisements",
#         null=False,
#         blank=False,
#     )
#     to_date = models.DateTimeField(
#         validators=(validate_current_and_future_month,),
#     )
#     date = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         verbose_name = "объявление услуги"
#         verbose_name_plural = "объявления услуг"
#
