from django.contrib.postgres.fields import ArrayField

from core.constants import Default, Messages, Limits
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from core.validators import RangeValueValidator, validate_age
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
    age = ArrayField(
            models.PositiveSmallIntegerField(),
            null=True,
            size=2,
        validators = [validate_age, ]
        )

    weight = models.CharField(max_length=10, choices=Default.WEIGHT_CHOICES)
    is_sterilized = models.BooleanField(default=False)
    is_vaccinated = models.BooleanField(default=False)
    owner = models.ForeignKey(
        CustomerProfile,
        verbose_name="владелец питомца",
        related_name="pets",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "питомец"
        verbose_name_plural = "питомцы"
        constraints = [
            UniqueConstraint(
                fields=["name", "breed", "age", "type",],
                name="unique_name_for_pet",
            ),
        ]

    def __str__(self) -> str:
        return (
            f"{self.type} {self.breed} {self.name} "
            f"владельца {self.owner_id}"
        )
