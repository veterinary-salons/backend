from django.db.models import CheckConstraint, Q, F, JSONField
from icecream import ic
from rest_framework import serializers

from core.constants import Limits, Default
from django.contrib.auth import get_user_model
from django.db import models

from core.utils import default_booking_time
from core.validators import (
    validate_alphanumeric,
    validate_current_and_future_month,
    validate_cynology_fields,
    validate_vet_fields,
    validate_grooming_service,
    validate_grooming_fields,
    validate_shelter_fields,
    validate_letters,
    RangeValueValidator,
    validate_shelter_service,
)
from pets.models import Pet
from users.models import SupplierProfile, CustomerProfile

User = get_user_model()


class Service(models.Model):
    """Модель услуг."""

    ad_title = models.CharField(
        max_length=Limits.MAX_LEN_TITLE_NAME,
        null=False,
        blank=False,
        validators=[validate_alphanumeric],
    )
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
        upload_to="images/",
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
        """Проверяем соответствие типа специалиста и услуг."""
        category = self.category
        service_name = self.extra_fields.get("service_name")

        if category == Default.SERVICES[0][0]:
            validate_cynology_fields(self)
        elif category == Default.SERVICES[1][0]:
            validate_vet_fields(self)
        elif category == Default.SERVICES[2][0]:
            validate_shelter_fields(self)
            validate_shelter_service(service_name)
        elif category == Default.SERVICES[3][0]:
            validate_grooming_service(service_name)
            validate_grooming_fields(self)

        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Service, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.extra_fields.get('service_name')} - {self.ad_title}"


class Price(models.Model):
    """Стоимость услуги."""

    customer = models.ManyToManyField(
        CustomerProfile,
        related_name="prices",
        verbose_name="клиенты",
        through="Booking",
    )
    service_name = models.CharField(
        max_length=Limits.MAX_LEN_SERVICE_NAME,
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
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="prices",
        null=False,
        blank=False,
    )

    def clean(self):
        """Проверяем соответствие типа специалиста и типа питомца."""
        if not self.service_name in self.service.extra_fields.get(
            "service_name"
        ):
            raise serializers.ValidationError(
                "Поле `service_name` в `price` должно быть в `service_name` в "
                "`extra_fields`."
            )
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Price, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "стоимость услуги"
        verbose_name_plural = "стоимости услуг"
        constraints = (
            CheckConstraint(
                check=Q(cost_from__lte=F("cost_to")),
                name="cost_range",
            ),
        )

    def __str__(self):
        return f"{self.service_name}: {self.cost_from} - {self.cost_to}"


class Booking(models.Model):
    """Модель бронирования услуги.

    Связываются `service`, `customer` и `supplier`.
    """

    description = models.TextField(
        max_length=Limits.MAX_LEN_DESCRIPTION,
    )
    price = models.ForeignKey(
        Price,
        on_delete=models.CASCADE,
        related_name="bookings",
    )
    customer = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name="bookings",
        verbose_name="пользователь",
        blank=False,
        null=False,
    )
    date = models.DateTimeField(auto_now_add=True)
    to_date = models.DateTimeField(
        validators=(validate_current_and_future_month,),
        blank=False,
        null=False,
        default=default_booking_time,
    )
    is_active = models.BooleanField(
        verbose_name="активно или нет",
        default=False,
    )
    is_confirmed = models.BooleanField(
        verbose_name="подтверждено или нет",
        default=False,
    )
    is_done = models.BooleanField(
        verbose_name="окончено или нет",
        default=False,
    )
    is_cancelled = models.BooleanField(
        verbose_name="отменено или нет",
        default=False,
    )

    class Meta:
        verbose_name = "бронь услуги"
        verbose_name_plural = "брони услуг"

    def __str__(self):
        return f"{self.price} - {self.date}"


class Review(models.Model):
    text = models.TextField(max_length=Limits.MAX_LEN_REVIEW)
    rating = models.PositiveSmallIntegerField(
        validators=[RangeValueValidator(Limits.MIN_RATING, Limits.MAX_RATING)],
    )
    customer = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="services",
    )
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "отзыв"
        verbose_name_plural = "отзывы"

    def __str__(self):
        return f"Отзыв {self.text[:20]} - {self.rating} - {self.date} на {self.service}"


class Favorite(models.Model):
    """Избранные услуги.

    Модель связывает `Price` и  `Customer`.
    """

    service = models.ForeignKey(
        Service,
        verbose_name="понравившиеся услуги",
        related_name="in_favorites",
        on_delete=models.CASCADE,
    )
    customer = models.ForeignKey(
        CustomerProfile,
        verbose_name="заказчик",
        related_name="in_favorites",
        on_delete=models.CASCADE,
    )
    date_added = models.DateTimeField(
        verbose_name="дата добавления",
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        verbose_name = "избранная услуга"
        verbose_name_plural = "избранные услуги"
        constraints = (
            # UniqueConstraint(
            #     fields=(
            #         "service",
            #         "customer",
            #     ),
            #     name="%(app_label)s_%(class)s услуга уже в избранном",
            # ),
        )

    def __str__(self) -> str:
        return f"{self.customer} -> {self.service}"


class FavoriteArticles(models.Model):
    """Избранные статьи."""

    article_id = models.PositiveIntegerField(
        validators=[RangeValueValidator(1, Limits.MAX_ARTICLE_ID_NUMBER)]
    )
    customer = models.ForeignKey(
        CustomerProfile,
        on_delete=models.CASCADE,
        related_name="favorite_articles",
    )
    date_added = models.DateTimeField(
        verbose_name="дата добавления",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "избранные статьи"
        verbose_name_plural = "избранные статьи"
