from django.core.exceptions import ValidationError
from django.utils import timezone

from core.constants import Default, Messages, Limits
from core.utils import grooming_type_default, synology_type_default
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator
from django.db import models

from core.validators import validate_letters, validate_alphanumeric
from pets.models import Pet
from users.models import SupplierProfile, CustomerProfile

User = get_user_model()


class BaseService(models.Model):
    name = models.CharField(
        verbose_name="название услуги",
        max_length=Limits.MAX_LEN_ANIMAL_TYPE,
        choices=Default.SERVICES,
        null=False,
        blank=False,
        validators=(validate_letters,),
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
        default="dog",
    )
    price = models.PositiveSmallIntegerField(
        verbose_name="Цена за услугу",
        default=Default.SERVICER_PRICE,
        validators=(
            MaxValueValidator(
                Limits.MAX_PRICE,
                Messages.CORRECT_AGE_MESSAGE,
            ),
        ),
    )
    duration = models.PositiveIntegerField(
        verbose_name="Продолжительность услуги в минутах",
        validators=(
            MaxValueValidator(
                Limits.MAX_DURATION,
                Messages.CORRECT_DURATION_MESSAGE,
            ),
        ),
    )
    work_time_from = models.TimeField(
        verbose_name="От",
        default="00:00:00",
    )
    work_time_to = models.TimeField(
        verbose_name="До",
        default="23:59:59",
    )
    format = ArrayField(
        models.CharField(
            max_length=50,
            choices=Default.SYNOLOGY_FORMAT,
            # default=DEFAULT.SYNOLOGY_FORMAT[0],
            validators=(validate_letters,),
        ),
        null=True,
        blank=True,
    )
    task = ArrayField(
        models.CharField(
            max_length=50,
            choices=Default.SYNOLOGY_TASKS,
        ),
        default=synology_type_default,
        null=True,
        blank=True,
    )
    grooming_type = ArrayField(
        models.CharField(
            max_length=20,
            choices=Default.GROOMING_TYPE,
            validators=(validate_letters,),
        ),
        default=grooming_type_default,
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

    def clean(self):
        super().clean()

        if self.name == Default.SERVICES[0] and self.pet_type != "dog":
            raise ValidationError("Кинолог работает только с собаками.")
        if self.name != Default.SERVICES[0] and any(
            (
                self.task,
                self.format,
            )
        ):
            raise ValidationError(
                "Поля `task` и `format` только для Кинолога."
            )
        if self.name != Default.SERVICES[3] and self.grooming_type:
            raise ValidationError("Поле `grooming_type` только для Грумера.")
        if self.name == Default.SERVICES[3] and not self.grooming_type:
            raise ValidationError("Поле `grooming_type` необходимо заполнить.")
        if self.name == Default.SERVICES[0] and not any(
            (
                self.task,
                self.format,
            )
        ):
            raise ValidationError(
                "Поле `task` и `format` необходимо заполнить."
            )
class BookingService(BaseService):
    """Модель бронирования услуги."""

    favour = models.CharField(
        max_length=20,
        choices=Default.SERVICES,
    )
    date = models.DateTimeField(auto_now_add=True)
    place = models.CharField(max_length=Limits.PLACE_MAX_LENGTH)
    client = models.ForeignKey(
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
