from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from core.constants import DEFAULT, Limits, MESSAGES
from pets.models import Pet

User = get_user_model()


class Specialist(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Специалист",
        on_delete=models.CASCADE,
        related_name="specialists",
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
        verbose_name="О себе"
    )


class Groomer(Specialist):
    pet_type = models.ForeignKey(
        Pet,
        verbose_name="тип животного",
        related_name="specialists",
        on_delete=models.SET_NULL,
        default=Pet(type="Dog")
    )
    # будет работать только на postgres
    grooming_type = ArrayField(models.CharField(
        max_length=1,
        choices=DEFAULT.GROOMING_TYPE,
        default=DEFAULT.GROOMING_TYPE[0]
    )
    )
    duration = models.PositiveIntegerField(
        verbose_name="Продолжительность услуги в минутах",
    )

    class Meta:
        verbose_name = 'грумер'
        verbose_name_plural = 'грумеры'

    def __str__(self) -> str:
        if self.user:
            return f'Грумер {self.user.second_name} {self.user.first_name}'
        return f'Грумер был удален'


class Veterinary(Specialist):
    pet_type = models.ForeignKey(
        Pet,
        verbose_name="тип животного",
        related_name="specialists",
        on_delete=models.SET_NULL,
        default=Pet(type="Dog")
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
        return f'Ветеринар был удален'


class Shelter(Specialist):
    pet_type = models.ForeignKey(
        Pet,
        verbose_name="тип животного",
        related_name="specialists",
        on_delete=models.SET_NULL,
        default=Pet(type="Dog")
    )

    class Meta:
        verbose_name = 'зооняня'
        verbose_name_plural = 'зооняни'

    def __str__(self) -> str:
        if self.user:
            return f'Зооняня {self.user.second_name} {self.user.first_name}'
        return f'Зооняня была удалена'


class Synology(Specialist):
    task = ArrayField(models.CharField(
        max_length=1,
        choices=DEFAULT.SYNOLOGY_TASKS,
        default=DEFAULT.SYNOLOGY_TASKS[0]
    )
    )
    format = ArrayField(models.CharField(
        max_length=1,
        choices=DEFAULT.SYNOLOGY_FORMAT,
        default=DEFAULT.SYNOLOGY_FORMAT[0],
    )
    )
    duration = models.PositiveIntegerField(
        verbose_name="Продолжительность услуги в минутах",
    )

