# Generated by Django 4.2.4 on 2023-11-15 08:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="customerprofile",
            old_name="photo",
            new_name="image",
        ),
        migrations.RenameField(
            model_name="supplierprofile",
            old_name="photo",
            new_name="image",
        ),
        migrations.AlterField(
            model_name="supplierprofile",
            name="pet_type",
            field=models.CharField(max_length=30, verbose_name="тип животного"),
        ),
    ]
