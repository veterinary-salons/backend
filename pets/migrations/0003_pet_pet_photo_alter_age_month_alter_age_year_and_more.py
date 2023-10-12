# Generated by Django 4.2.4 on 2023-10-12 16:52

import core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
        ("pets", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="pet",
            name="pet_photo",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
        migrations.AlterField(
            model_name="age",
            name="month",
            field=models.PositiveSmallIntegerField(
                blank=True,
                null=True,
                validators=[core.validators.RangeValueValidator(0, 11)],
            ),
        ),
        migrations.AlterField(
            model_name="age",
            name="year",
            field=models.PositiveIntegerField(
                blank=True,
                null=True,
                validators=[core.validators.RangeValueValidator(0, 50)],
            ),
        ),
        migrations.AlterField(
            model_name="pet",
            name="age",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="pets",
                to="pets.age",
            ),
        ),
        migrations.AlterField(
            model_name="pet",
            name="is_sterilized",
            field=models.CharField(
                choices=[("Да", "Да"), ("Нет", "Нет"), ("Не знаю", "Не знаю")],
                default="Не знаю",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="pet",
            name="is_vaccinated",
            field=models.CharField(
                choices=[("Да", "Да"), ("Нет", "Нет"), ("Не знаю", "Не знаю")],
                default="Не знаю",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="pet",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pet",
                to="users.customerprofile",
                verbose_name="владелец питомца",
            ),
        ),
        migrations.AlterField(
            model_name="pet",
            name="weight",
            field=models.FloatField(
                validators=[core.validators.RangeValueValidator(0, 200)]
            ),
        ),
        migrations.AddConstraint(
            model_name="age",
            constraint=models.CheckConstraint(
                check=models.Q(("year__gt", 0), ("month__gt", 0), _connector="OR"),
                name="year_or_month_not_zero",
            ),
        ),
    ]
