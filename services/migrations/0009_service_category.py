# Generated by Django 4.2.4 on 2023-10-23 08:23

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0008_remove_booking_name_remove_service_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="category",
            field=models.CharField(
                choices=[
                    ("cynology", "Кинолог"),
                    ("veterenary", "Ветеринар"),
                    ("shelter", "Зооняня"),
                    ("grooming", "Грумер"),
                ],
                default="cynology",
                max_length=30,
                validators=[core.validators.validate_letters],
                verbose_name="тип услуги",
            ),
            preserve_default=False,
        ),
    ]
