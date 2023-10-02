# Generated by Django 4.2.4 on 2023-09-30 09:12

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0004_remove_bookingservice_name_remove_service_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookingservice",
            name="name",
            field=models.CharField(
                choices=[
                    ("Synology", "Кинолог"),
                    ("Veterenary", "Ветеринар"),
                    ("Shelter", "Зооняня"),
                    ("groomer", "Грумер"),
                ],
                default="asdf",
                max_length=30,
                validators=[core.validators.validate_letters],
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="service",
            name="name",
            field=models.CharField(
                choices=[
                    ("Synology", "Кинолог"),
                    ("Veterenary", "Ветеринар"),
                    ("Shelter", "Зооняня"),
                    ("groomer", "Грумер"),
                ],
                default="sdf",
                max_length=30,
                validators=[core.validators.validate_letters],
            ),
            preserve_default=False,
        ),
    ]
