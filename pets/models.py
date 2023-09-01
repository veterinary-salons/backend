from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.utils import timezone

from core.constants import Limits, MESSAGES, DEFAULT

User = get_user_model()


class Pet(models.Model):
    """Характеристика животного.

    Связано с моделью User через Foreigkey.

    Attributes:
        type (str):
            Вид питомца (кошка, собака и т.д.).
        breed (str):
            Порода питомца.
        name (str):
            Имя питомца.
        age (int):
            Возраст питомца. Должен быть положительным целым числом,
            находящимся в заданных пределах.
        weight (str):
            Категория веса питомца.
        is_sterilized (bool):
            Указывает, стерилизовано ли животное.
        is_vaccinated (bool):
            Указывает, привито ли животное.
        owner (User):
            Владелец питомца.

    """
    type = models.CharField(
        verbose_name="вид питомца",
        max_length=Limits.MAX_LEN_ANIMAL_TYPE,
    )
    breed = models.CharField(
        verbose_name="порода",
        max_length=Limits.MAX_LEN_ANIMAL_BREED,
    )
    name = models.CharField(
        verbose_name="имя питомца",
        max_length=Limits.MAX_LEN_ANIMAL_NAME,
    )
    age = models.PositiveSmallIntegerField(
        verbose_name="Возраст питомца",
        default=DEFAULT.PET_AGE,
        validators=(
            MinValueValidator(
                Limits.MIN_AGE_PET,
                MESSAGES.CORRECT_AGE_MESSAGE,
            ),
            MaxValueValidator(
                Limits.MAX_AGE_PET,
                MESSAGES.CORRECT_AGE_MESSAGE,
            ),
        ),
    )
    weight = models.CharField(max_length=1, choices=DEFAULT.WEIGHT_CHOICES)
    is_sterilized = models.BooleanField(default=False)
    is_vaccinated = models.BooleanField(default=False)
    owner = models.ForeignKey(
        User,
        verbose_name="владелец питомца",
        related_name="pets",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "питомец"
        verbose_name_plural = "питомцы"
        ordering = ("name",)
        constraints = (
            UniqueConstraint(
                fields=(
                    "name",
                    "breed",
                    "type",
                    "age",
                    'owner'
                ),
                name="unique_for_pet",
            ),
        )

    def __str__(self) -> str:
        return f"{self.type} {self.breed} {self.name} владельца {self.owner.second_name}"


class Specialist(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Специалист",
        on_delete=models.CASCADE,
        related_name="specialists",
    )
    pet_type = models.ForeignKey(
        Pet,
        verbose_name="тип животного",
        related_name="specialists",
        on_delete=models.SET_NULL,
        default=Pet(type="Dog")
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
    duration = models.PositiveIntegerField(
        verbose_name="Продолжительность услуги в минутах",
    )
    about = models.TextField(
        max_length=Limits.MAX_LENGTH_ABOUT,
        verbose_name="О себе"
    )


class Groomer(Specialist):
    # будет работать только на postgres
    grooming_type = ArrayField(models.CharField(
        max_length=1,
        choices=DEFAULT.GROOMING_TYPE,
        default=DEFAULT.GROOMING_TYPE[0]
    )
    )

    class Meta:
        verbose_name = 'грумер'
        verbose_name_plural = 'грумеры'

    def __str__(self) -> str:
        if self.user:
            return f'Грумер {self.user.second_name} {self.user.first_name}'
        return f'Грумер был удален'


class Veterinary(models.Model):
    ...


class Shelter(models.Model):
    ...


class Synology(models.Model):
    ...
