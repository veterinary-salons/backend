from core.constants import Default, Messages, Limits
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from users.models import CustomerProfile


class Animal(models.Model):
    """Характеристика животного."""

    type = models.CharField(
        verbose_name="вид животного",
        max_length=Limits.MAX_LEN_ANIMAL_TYPE,
        choices=Default.PET_TYPE,
    )
    class Meta:
        abstract = True
        verbose_name = "характеристика животного"
        verbose_name_plural = "характеристики животных"

class Pet(Animal):
    """Характеристика питомца.

    Связано с моделью CustomerProfile через Foreigkey.

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
    )
    name = models.CharField(
        verbose_name="имя питомца",
        max_length=Limits.MAX_LEN_ANIMAL_NAME,
    )
    age = models.PositiveSmallIntegerField(
        verbose_name="Возраст питомца",
        default=Default.PET_AGE,
        validators=(
            MinValueValidator(
                Limits.MIN_AGE_PET,
                Messages.CORRECT_AGE_MESSAGE,
            ),
            MaxValueValidator(
                Limits.MAX_AGE_PET,
                Messages.CORRECT_AGE_MESSAGE,
            ),
        ),
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
        ordering = ("name",)
        constraints = (
            UniqueConstraint(
                fields=("name", "breed", "type", "age", "owner"),
                name="unique_for_pet",
            ),
        )

    def __str__(self) -> str:
        return (
            f"{self.type} {self.breed} {self.name} "
            f"владельца {self.owner_id}"
        )
