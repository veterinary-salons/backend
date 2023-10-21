from django.db.models import UniqueConstraint, CheckConstraint, Q, F, JSONField
from django.utils import timezone
from icecream import ic
from rest_framework import serializers

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
    cost_from = models.DecimalField(
        decimal_places=0,
        max_digits=5,
        default=Default.COST_FROM,
        validators=[RangeValueValidator(Limits.MIN_PRICE, Limits.MAX_PRICE)],
    )
    cost_to = models.DecimalField(
        decimal_places=0,
        max_digits=5,
        default=Default.COST_TO,
        validators=[RangeValueValidator(Limits.MIN_PRICE, Limits.MAX_PRICE)],
    )
    extra_fields = JSONField()

    class Meta:
        verbose_name = "услуга"
        verbose_name_plural = "услуги"
        constraints = (
            CheckConstraint(
                check=Q(cost_from__lte=F("cost_to")),
                name="cost_range",
            ),
            # UniqueConstraint(
            #     fields=["name", "supplier"],
            #     name="unique_name_for_service",
            # )
        )

    def clean(self):
        """Проверяем соответствие типа специалиста и типа питомца."""
        if (
            self.supplier.specialist_type == Default.SERVICES[0][0]
            and self.extra_fields.service not in Default.CYNOLOGY_SERVICES
        ):
            raise serializers.ValidationError(
                f"У кинолога нет такой услуги: {self.extra_fields.service}. Выбор из услуг: {Default.CYNOLOGY_SERVICES}"
            )
        if (
            self.supplier.specialist_type == Default.SERVICES[1][0]
            and self.extra_fields.service not in Default.VET_SERVICES
        ):
            raise serializers.ValidationError(
                f"У ветеринара нет такой услуги: {self.extra_fields.service}. Выбор из услуг: {Default.VET_SERVICES}"
            )
        if (
            self.supplier.specialist_type == Default.SERVICES[2][0]
            and self.extra_fields.service not in Default.GROOMING_TYPE
        ):
            raise serializers.ValidationError(
                f"У грумера нет такой услуги: {self.extra_fields.service}. Выбор из услуг: {Default.GROOMING_TYPE}"
            )
        if (
            self.supplier.specialist_type == Default.SERVICES[3][0]
            and self.extra_fields.service != Default.SHELTER_SERVICE
        ):
            raise serializers.ValidationError(
                f"У зооняни нет такой услуги: {self.extra_fields.service}. Зооняня не "
                f"предлает других услуг, кроме. {Default.SHELTER_SERVICE} "
                f"единственное возможное значение для этого поля"
            )
        if self.supplier.specialist_type != Default.SERVICES[0][0] and any(
            (
                self.extra_fields.get("task"),
                self.extra_fields.get("formats"),
            )
        ):
            raise serializers.ValidationError(
                "Поля `task` и `formats` только для Кинолога."
            )
        if self.extra_fields.get("task") not in Default.CYNOLOGY_SERVICES:
            raise serializers.ValidationError(
                f"Поле `task` должно быть из списка услуг: {Default.CYNOLOGY_SERVICES}"
            )
        if self.extra_fields.get("format") not in Default.CYNOLOGY_FORMAT:
            raise serializers.ValidationError(
                f"Поле `format` должно быть из списка услуг: {Default.CYNOLOGY_FORMAT}"
            )
        if self.supplier.specialist_type != Default.SERVICES[3][
            0
        ] and self.extra_fields.get("grooming_type"):
            raise serializers.ValidationError(
                "Поле `grooming_type` только для Грумера."
            )
        if self.supplier.specialist_type == Default.SERVICES[3][
            0
        ] and not self.extra_fields.get("grooming_type"):
            raise serializers.ValidationError(
                "Поле `grooming_type` необходимо заполнить."
            )
        if self.supplier.specialist_type == Default.SERVICES[0][0] and not all(
            (
                self.extra_fields.get("task"),
                self.extra_fields.get("formats"),
            )
        ):
            raise serializers.ValidationError(
                "Поле `task` и `formats` необходимо заполнить."
            )
        if self.supplier.specialist_type == Default.SERVICES[
            1
        ] and not self.extra_fields.get("vet_services"):
            raise serializers.ValidationError(
                "Поле `vet_services` необходимо заполнить."
            )
        if self.supplier.specialist_type != Default.SERVICES[
            2
        ] and self.extra_fields.get("vet_services"):
            raise serializers.ValidationError(
                "Поле `vet_services` только для ветеринара."
            )
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
