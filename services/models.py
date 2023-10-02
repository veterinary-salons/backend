from django.db.models import UniqueConstraint
from django.utils import timezone

from core.constants import Default, Messages, Limits
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.db import models

from core.validators import (
    validate_letters,
    validate_alphanumeric,
    validate_services,
    RangeValueValidator,
    validate_current_and_future_month,
)
from pets.models import Pet
from users.models import SupplierProfile, CustomerProfile

User = get_user_model()


class BaseService(models.Model):
    name = models.CharField(
        verbose_name="название услуги",
        max_length=Limits.MAX_LEN_SERVICE_NAME,
        null=False,
        blank=False,
        validators=(validate_alphanumeric,),
    )
    service_type = models.CharField(
        verbose_name="тип услуги",
        max_length=Limits.MAX_LEN_SERVICE_TYPE,
        choices=Default.SERVICES,
        validators=(validate_letters,),
        blank=False,
        null=False,
    )
    supplier = models.ForeignKey(
        SupplierProfile,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True


class Service(BaseService):
    pet_type = models.CharField(
        verbose_name="тип животного",
        max_length=Limits.MAX_LEN_ANIMAL_TYPE,
        choices=Default.PET_TYPE,
    )
    price = models.PositiveSmallIntegerField(
        verbose_name="Цена за услугу",
        default=Default.SERVICER_PRICE,
        validators=[
            RangeValueValidator(
                Limits.MIN_PRICE,
                Limits.MAX_PRICE,
            ),
        ],
    )
    duration = models.PositiveIntegerField(
        validators=[
            RangeValueValidator(
                Limits.MIN_DURATION,
                Limits.MAX_DURATION,
            ),
        ]
    )
    work_time_from = models.TimeField(
        verbose_name="От",
        default="00:00:00",
    )
    work_time_to = models.TimeField(
        verbose_name="До",
        default="23:59:59",
    )
    formats = ArrayField(
        models.CharField(
            max_length=50,
            choices=Default.CYNOLOGY_FORMAT,
            validators=(validate_letters,),
        ),
        null=True,
        blank=True,
    )
    task = ArrayField(
        models.CharField(
            max_length=50,
        ),
        null=True,
        blank=True,
    )
    grooming_type = ArrayField(
        models.CharField(
            max_length=20,
            choices=Default.GROOMING_TYPE,
            validators=(validate_letters,),
        ),
        null=True,
        blank=True,
    )
    about = models.TextField(
        max_length=Limits.MAX_LENGTH_ABOUT,
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
        super().clean()
        validate_services(
            self.service_type,
            self.pet_type,
            self.task,
            self.formats,
            self.grooming_type,
        )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Service, self).save(*args, **kwargs)


class BookingService(BaseService):
    """Модель бронирования услуги."""

    favour = models.CharField(
        choices=Default.SERVICES,
    )
    date = models.DateTimeField(auto_now_add=True)
    to_date = models.DateTimeField(
        validators=(validate_current_and_future_month,),
        blank=False,
        null=False,
        default=timezone.now,
    )
    place = models.CharField(
        max_length=Limits.PLACE_MAX_LENGTH, blank=True, null=True,
        validators=(validate_alphanumeric,),
    )
    customer = models.ForeignKey(
        CustomerProfile,
        models.CASCADE,
        null=False,
        blank=False,
    )
    confirmed = models.BooleanField(
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
