# Generated by Django 4.2.4 on 2023-11-24 09:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0004_price_time_per_visit_alter_service_image"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="favorite",
            constraint=models.UniqueConstraint(
                fields=("service", "customer"),
                name="services_favorite услуга уже в избранном",
            ),
        ),
    ]
