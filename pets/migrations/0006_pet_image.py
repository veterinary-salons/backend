# Generated by Django 4.2.4 on 2023-11-15 17:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pets", "0005_remove_pet_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="pet",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
    ]
