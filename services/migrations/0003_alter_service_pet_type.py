# Generated by Django 4.2.4 on 2023-09-30 09:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "services",
            "0002_alter_bookingservice_date_alter_bookingservice_name_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="service",
            name="pet_type",
            field=models.CharField(
                choices=[
                    ("cat", "Кошка"),
                    ("dog", "Собака"),
                    ("pig", "Морская свинка"),
                    ("hom", "Хомяк"),
                    ("ano", "Другое"),
                ],
                max_length=30,
                verbose_name="тип животного",
            ),
        ),
    ]
