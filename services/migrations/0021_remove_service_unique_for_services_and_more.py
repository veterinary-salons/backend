# Generated by Django 4.2.4 on 2023-10-09 16:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0020_remove_bookingservice_specialist_type_and_more"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="service",
            name="unique_for_services",
        ),
        migrations.AddConstraint(
            model_name="service",
            constraint=models.UniqueConstraint(
                fields=("name", "supplier", "booking"), name="unique_for_services"
            ),
        ),
    ]
