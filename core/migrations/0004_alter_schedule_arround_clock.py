# Generated by Django 4.2.4 on 2023-11-13 15:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_alter_schedule_time_per_visit"),
    ]

    operations = [
        migrations.AlterField(
            model_name="schedule",
            name="arround_clock",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
