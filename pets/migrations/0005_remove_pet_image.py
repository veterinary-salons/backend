# Generated by Django 4.2.4 on 2023-11-15 17:04

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("pets", "0004_alter_animal_type_alter_pet_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="pet",
            name="image",
        ),
    ]
