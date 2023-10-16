from django.db import models

from core.constants import Default
from services.models import Service
from users.models import SupplierProfile


class Schedule(models.Model):
    """Расписание специалиста."""

    weekday = models.IntegerField(
        choices=Default.DAYS_OF_WEEK,
        verbose_name="День недели",
        null=False,
        blank=False,
    )
    is_working_day = models.BooleanField(
        default=True, verbose_name="Рабочий день"
    )
    start_work_time = models.TimeField(
        verbose_name="Время начала работы", default="09:00:00"
    )
    end_work_time = models.TimeField(
        verbose_name="Время окончания работы", default="19:00:00"
    )
    break_start_time = models.TimeField(
        verbose_name="Время начала перерыва",
        null=True,
        blank=True,
        default="13:00:00",
    )
    break_end_time = models.TimeField(
        verbose_name="Время окончания перерыва",
        null=True,
        blank=True,
        default="14:00:00",
    )
    supplier = models.ForeignKey(
        SupplierProfile,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = "расписание специалиста"
