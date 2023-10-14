from django.contrib.postgres.fields import ArrayField
from django.db import models

from core.constants import Default
from core.validators import RangeValueValidator


class OutDoor(models.Model):
    """Модель для выездов."""

    out = models.BooleanField(default=False)

    class Meta:
        verbose_name = "выезд"
        verbose_name_plural = "выезды"


class Schedule(models.Model):
    """Расписание специалиста."""

    hours = {}
    for day, label in Default.DAYS_OF_WEEK:
        hours[label.lower()] = ArrayField(
            models.PositiveSmallIntegerField(
                validators=[RangeValueValidator(0, 24)]
            ),
            null=True,
            size=2,
        )
    breakTime = ArrayField(
        models.PositiveSmallIntegerField(
            validators=[RangeValueValidator(0, 24)]
        ),
        null=True,
        size=2,
    )
    monday_hours = hours[Default.DAYS_OF_WEEK[0][1].lower()]
    tuesday_hours = hours[Default.DAYS_OF_WEEK[1][1].lower()]
    wednesday_hours = hours[Default.DAYS_OF_WEEK[2][1].lower()]
    thursday_hours = hours[Default.DAYS_OF_WEEK[3][1].lower()]
    friday_hours = hours[Default.DAYS_OF_WEEK[4][1].lower()]
    saturday_hours = hours[Default.DAYS_OF_WEEK[5][1].lower()]
    sunday_hours = hours[Default.DAYS_OF_WEEK[6][1].lower()]

    class Meta:
        verbose_name = "расписание специалиста"
