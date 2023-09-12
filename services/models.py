from core.constants import DEFAULT, MESSAGES, Limits
from core.utils import grooming_type_default, synology_type_default
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from pets.models import Pet
from users.models import SupplierProfile


class Specialist(models.Model):
    """Абстрактная базовая модель объявления."""

    pet_type = models.CharField(
        verbose_name="тип животного",
        max_length=Limits.MAX_LEN_ANIMAL_TYPE,
        choices=DEFAULT.PET_TYPE,
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
    work_time_from = models.DateTimeField(
        verbose_name="От",
        default=timezone.now,
    )
    work_time_to = models.DateTimeField(
        verbose_name="До",
        default=timezone.now,
    )
    about = models.TextField(
        max_length=Limits.MAX_LENGTH_ABOUT,
        verbose_name="О себе",
        blank=True,
        null=True,
    )
    published = models.BooleanField(
        default=True,
    )

    class Meta:
        abstract = True


class Groomer(Specialist):
    """Модель объявления грумера."""

    supplier = models.ForeignKey(
        SupplierProfile,
        on_delete=models.CASCADE,
        related_name="grooming"
    )

    # будет работать только на postgres
    grooming_type = ArrayField(
        models.CharField(
            max_length=20,
            choices=DEFAULT.GROOMING_TYPE,
        ),
        default=grooming_type_default,
    )
    duration = models.PositiveIntegerField(
        verbose_name="Продолжительность услуги в минутах",
    )

    class Meta:
        verbose_name = 'грумер'
        verbose_name_plural = 'грумеры'

    def __str__(self) -> str:
        if self.user:
            return f'Грумер {self.user} {self.user}'
        return 'Грумер был удален'


class Veterinary(Specialist):
    """Модель объявления ветеринара."""

    supplier = models.ForeignKey(
        SupplierProfile,
        on_delete=models.CASCADE,
        related_name="veterinary"
    )

    duration = models.PositiveIntegerField(
        verbose_name="Продолжительность услуги в минутах",
    )

    class Meta:
        verbose_name = 'ветеринар'
        verbose_name_plural = 'ветеринары'

    def __str__(self) -> str:
        if self.user:
            return f'Ветеринар {self.user.second_name} {self.user.first_name}'
        return 'Ветеринар был удален'


class Shelter(Specialist):
    """Модель объявления зооняни(передержка)."""

    supplier = models.ForeignKey(
        SupplierProfile,
        on_delete=models.CASCADE,
        related_name="shelter"
    )

    class Meta:
        verbose_name = 'зооняня'
        verbose_name_plural = 'зооняни'

    def __str__(self) -> str:
        if self.user:
            return f'Зооняня {self.user.second_name} {self.user.first_name}'
        return 'Зооняня была удалена'


class Synology(Specialist):
    """Модель объявления кинолога."""

    supplier = models.ForeignKey(
        SupplierProfile,
        on_delete=models.CASCADE,
        related_name="cynology"
    )
    pet_type = None
    task = ArrayField(
        models.CharField(
            max_length=50,
            choices=DEFAULT.SYNOLOGY_TASKS,
        ),
        default=synology_type_default,
    )
    format = ArrayField(
        models.CharField(
            max_length=50,
            choices=DEFAULT.SYNOLOGY_FORMAT,
            default=DEFAULT.SYNOLOGY_FORMAT[0],
        ),
    )
    duration = models.PositiveIntegerField(
        verbose_name="Продолжительность услуги в минутах",
    )

    class Meta:
        verbose_name = 'кинолог'
        verbose_name_plural = 'кинологи'

    def __str__(self) -> str:
        if self.user:
            return f"Кинолог {self.user}"
        return 'Кинолог был удален'
