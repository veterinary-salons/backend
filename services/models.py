from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

from core.constants import DEFAULT, Limits, MESSAGES
from core.utils import grooming_type_default, synology_type_default
from pets.models import Pet

User = get_user_model()


class Specialist(models.Model):
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
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    pet_type = models.ForeignKey(
        Pet,
        verbose_name="тип животного",
        related_name="groomers",
        on_delete=models.CASCADE,
    )

    # будет работать только на postgres
    grooming_type = ArrayField(models.CharField(
        max_length=20,
        choices=DEFAULT.GROOMING_TYPE,
    ),
        default=grooming_type_default
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
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    pet_type = models.ForeignKey(
        Pet,
        verbose_name="тип животного",
        related_name="veterinarys",
        on_delete=models.CASCADE,
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
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    pet_type = models.ForeignKey(
        Pet,
        verbose_name="тип животного",
        related_name="shelters",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'зооняня'
        verbose_name_plural = 'зооняни'

    def __str__(self) -> str:
        if self.user:
            return f'Зооняня {self.user.second_name} {self.user.first_name}'
        return f'Зооняня была удалена'


class Synology(Specialist):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    task = ArrayField(models.CharField(
        max_length=50,
        choices=DEFAULT.SYNOLOGY_TASKS,
    ),
        default=synology_type_default
    )
    format = ArrayField(models.CharField(
        max_length=50,
        choices=DEFAULT.SYNOLOGY_FORMAT,
        default=DEFAULT.SYNOLOGY_FORMAT[0],
    )
    )
    duration = models.PositiveIntegerField(
        verbose_name="Продолжительность услуги в минутах",
    )
