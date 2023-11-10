# Generated by Django 4.2.4 on 2023-10-30 09:48

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("users", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="Age",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "year",
                    models.PositiveIntegerField(
                        validators=[django.core.validators.MaxValueValidator(50)]
                    ),
                ),
                (
                    "month",
                    models.PositiveSmallIntegerField(
                        validators=[django.core.validators.MaxValueValidator(11)]
                    ),
                ),
            ],
            options={
                "verbose_name": "возраст питомца",
                "verbose_name_plural": "возрасты питомцев",
            },
        ),
        migrations.CreateModel(
            name="Animal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("dog", "Собака"),
                            ("cat", "Кошка"),
                            ("pig", "Морская свинка"),
                            ("hom", "Хомяк"),
                            ("hor", "Хорек"),
                            ("rab", "Кролик"),
                            ("ano", "Другое"),
                        ],
                        max_length=30,
                        verbose_name="вид животного",
                    ),
                ),
            ],
            options={
                "verbose_name": "характеристика животного",
                "verbose_name_plural": "характеристики животных",
            },
        ),
        migrations.CreateModel(
            name="Pet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("dog", "Собака"),
                            ("cat", "Кошка"),
                            ("pig", "Морская свинка"),
                            ("hom", "Хомяк"),
                            ("hor", "Хорек"),
                            ("rab", "Кролик"),
                            ("ano", "Другое"),
                        ],
                        max_length=30,
                        verbose_name="вид животного",
                    ),
                ),
                (
                    "breed",
                    models.CharField(
                        blank=True, max_length=30, null=True, verbose_name="порода"
                    ),
                ),
                ("name", models.CharField(max_length=30, verbose_name="имя питомца")),
                (
                    "weight",
                    models.CharField(
                        choices=[
                            ("1", "до 5кг."),
                            ("2", "5 - 10кг."),
                            ("3", "10 - 20кг."),
                            ("4", "более 20кг."),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "is_sterilized",
                    models.CharField(
                        choices=[
                            ("Да", "Стерилизован"),
                            ("Нет", "Не стерилизован"),
                            ("Не знаю", "Не знаю"),
                        ],
                        default="Да",
                        max_length=10,
                    ),
                ),
                (
                    "is_vaccinated",
                    models.CharField(
                        choices=[
                            ("Да", "Вакцинирован"),
                            ("Нет", "Не вакцинирован"),
                            ("Не знаю", "Не знаю"),
                        ],
                        default="Да",
                        max_length=10,
                    ),
                ),
                (
                    "age",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="pets.age",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pet",
                        to="users.customerprofile",
                        verbose_name="владелец питомца",
                    ),
                ),
            ],
            options={
                "verbose_name": "питомец",
                "verbose_name_plural": "питомцы",
            },
        ),
        migrations.AddConstraint(
            model_name="pet",
            constraint=models.UniqueConstraint(
                fields=("name", "breed", "age", "type"), name="unique_name_for_pet"
            ),
        ),
    ]
