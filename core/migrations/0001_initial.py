# Generated by Django 4.2.4 on 2023-11-11 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("services", "__first__"),
    ]

    operations = [
        migrations.CreateModel(
            name="Schedule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "weekday",
                    models.CharField(
                        choices=[
                            ("Пн.", "Понедельник"),
                            ("Вт.", "Вторник"),
                            ("Ср.", "Среда"),
                            ("Чт.", "Четверг"),
                            ("Пт.", "Пятница"),
                            ("Сб.", "Суббота"),
                            ("Вс.", "Воскресенье"),
                        ],
                        verbose_name="День недели",
                    ),
                ),
                (
                    "is_working_day",
                    models.BooleanField(default=True, verbose_name="Рабочий день"),
                ),
                (
                    "start_work_time",
                    models.TimeField(
                        default="09:00:00", verbose_name="Время начала работы"
                    ),
                ),
                (
                    "end_work_time",
                    models.TimeField(
                        default="19:00:00", verbose_name="Время окончания работы"
                    ),
                ),
                (
                    "break_start_time",
                    models.TimeField(
                        blank=True,
                        default="14:00:00",
                        null=True,
                        verbose_name="Время начала перерыва",
                    ),
                ),
                (
                    "break_end_time",
                    models.TimeField(
                        blank=True,
                        default="14:00:00",
                        null=True,
                        verbose_name="Время окончания перерыва",
                    ),
                ),
                (
                    "time_per_visit",
                    models.DecimalField(
                        choices=[(0.5, 0.5), (1.0, 1.0), (1.5, 1.5), (2.0, 2.0)],
                        decimal_places=1,
                        default=0.5,
                        max_digits=3,
                    ),
                ),
                ("arround_clock", models.BooleanField(default=False)),
                (
                    "service",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="schedules",
                        to="services.service",
                    ),
                ),
            ],
            options={
                "verbose_name": "расписание специалиста",
            },
        ),
    ]
