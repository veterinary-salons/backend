from django.contrib.postgres.fields import ArrayField

from core.classes import YesNoDontKnow
from core.constants import Default, Messages, Limits
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint, Q

from core.validators import RangeValueValidator
from users.models import CustomerProfile


class AnimalAbstract(models.Model):
    """Абстрактная модель животного.

    Необходимо, чтобы использовать поле `type` в UniqueConstraint.

    """

    type = models.CharField(
        verbose_name="вид животного",
        max_length=Limits.MAX_LEN_ANIMAL_TYPE,
        choices=Default.PET_TYPE,
    )

    class Meta:
        abstract = True

class Animal(AnimalAbstract):
    """Характеристика животного."""

    class Meta:
        verbose_name = "характеристика животного"
        verbose_name_plural = "характеристики животных"


class Age(models.Model):
    year = models.PositiveIntegerField(
        validators=[RangeValueValidator(0, Limits.MAX_AGE_PET)],
        null=True,
        blank=True,
    )
    month = models.PositiveSmallIntegerField(
        validators=[RangeValueValidator(0, Limits.MAX_MONTH_QUANTITY)],
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "возраст питомца"
        verbose_name_plural = "возрасты питомцев"
        constraints = [
            models.CheckConstraint(
                check=Q(year__gt=0) | Q(month__gt=0),
                name="year_or_month_not_zero",
            )
        ]


class Pet(AnimalAbstract):
    """Характеристика питомца.

    Связано с моделью `CustomerProfile` через `Foreignkey`.

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
        owner (CustomerProfile):
            Владелец питомца.

    """

    breed = models.CharField(
        verbose_name="порода",
        max_length=Limits.MAX_LEN_ANIMAL_BREED,
        null=True,
        blank=True,
    )
    name = models.CharField(
        verbose_name="имя питомца",
        max_length=Limits.MAX_LEN_ANIMAL_NAME,
    )
    age = models.ForeignKey(
        Age,
        on_delete=models.SET_NULL,
        null=True,
        related_name="pets",
    )
    pet_photo = models.ImageField(null=True, blank=True)
    weight = models.FloatField(
        validators=[RangeValueValidator(0, Limits.MAX_WEIGHT)]
    )
    is_sterilized = models.CharField(
        max_length=10,
        choices=YesNoDontKnow.choices,
        default=YesNoDontKnow.DONT_KNOW,
    )
    is_vaccinated = models.CharField(
        max_length=10,
        choices=YesNoDontKnow.choices,
        default=YesNoDontKnow.DONT_KNOW,
    )
    owner = models.ForeignKey(
        CustomerProfile,
        verbose_name="владелец питомца",
        related_name="pet",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "питомец"
        verbose_name_plural = "питомцы"
        constraints = [
            UniqueConstraint(
                fields=[
                    "name",
                    "breed",
                    "age",
                    "type",
                ],
                name="unique_name_for_pet",
            ),
        ]

    def __str__(self) -> str:
        return (
            f"{self.type} {self.breed} {self.name} "
            f"владельца {self.owner_id}"
        )
