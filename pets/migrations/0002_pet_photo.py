# Generated by Django 4.2.4 on 2023-10-30 10:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pets", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="pet",
            name="photo",
            field=models.ImageField(blank=True, null=True, upload_to=""),
        ),
    ]
