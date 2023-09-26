from django.core.exceptions import ValidationError

from core.constants import DEFAULT, MESSAGES, Limits
from core.utils import grooming_type_default, synology_type_default
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from pets.models import Pet
from users.models import SupplierProfile, CustomerProfile

User = get_user_model()

class BaseService(models.Model):
    name = models.CharField(
        verbose_name="название услуги",
        max_length=Limits.MAX_LEN_ANIMAL_TYPE,
        choices=DEFAULT.SERVICES,
        null = False,
        blank= False,
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
        choices=DEFAULT.PET_TYPE,
        default="dog",
    )
    price = models.PositiveSmallIntegerField(
        verbose_name="Цена за услугу",
        default=DEFAULT.SERVICER_PRICE,
        validators=(
            MinValueValidator(
                Limits.MIN_DURATION,
                MESSAGES.CORRECT_AGE_MESSAGE,
            ),
            MaxValueValidator(
                Limits.MAX_DURATION,
                MESSAGES.CORRECT_AGE_MESSAGE,
            ),
        ),
    )
    duration = models.PositiveIntegerField(
        verbose_name="Продолжительность услуги в минутах",
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
            choices=DEFAULT.SYNOLOGY_FORMAT,
            default=DEFAULT.SYNOLOGY_FORMAT[0],
        ),
        null = True,
        blank = True,
    )
    task = ArrayField(
        models.CharField(
            max_length=50,
            choices=DEFAULT.SYNOLOGY_TASKS,
        ),
        default=synology_type_default,
        null = True,
        blank = True
    )
    grooming_type = ArrayField(
        models.CharField(
            max_length=20,
            choices=DEFAULT.GROOMING_TYPE,
        ),
        default=grooming_type_default,
        null=True,
        blank=True,
    )

    def clean(self):
        super().clean()

        selected_services = sum(
            [
                self.groomer_id is not None,
                self.synology_id is not None,
                self.shelter_id is not None,
                self.veterinary_id is not None,
            ]
        )

        if selected_services != 1:
            raise ValidationError(
                "Одна и только одна услуга должна быть выбрана"
            )

class Announcement(Service):
    """Модель объявления."""

    about = models.TextField(
        max_length=Limits.MAX_LENGTH_ABOUT,
        verbose_name="О себе",
        blank=True,
        null=True,
    )
    published = models.BooleanField(
        default=False,
    )
    class Meta:
        verbose_name = "объявление"
        verbose_name_plural = "объявления"

class BookingService(BaseService):
    """Модель бронирования услуги."""

    favour = models.CharField(
        max_length = 20,
        choices = DEFAULT.SERVICES,
    )
    date = models.DateField()
    place = models.CharField(max_length=Limits.PLACE_MAX_LENGTH)
    client = models.ForeignKey(
        CustomerProfile,
        models.CASCADE,
        null=False,
        blank=False,
    )

    confirmed = models.BooleanField(verbose_name="подтверждено или нет", default=False,)
    actual = models.BooleanField(verbose_name="активно или нет", default=False,)

    class Meta:
        verbose_name = "бронь услуги"
        verbose_name_plural = "брони услуг"
