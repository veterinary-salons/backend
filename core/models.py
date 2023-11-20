from django.db import models

from core.constants import Default
from services.models import Service
from users.models import SupplierProfile


class Schedule(models.Model):
    """Расписание услуги."""

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="schedules",
        null=False,
        blank=False,
    )
    weekday = models.CharField(
        choices=Default.DAYS_OF_WEEK,
        verbose_name="День недели",
        null=False,
        blank=False,
    )
    break_end_time  = models.TimeField(
        verbose_name="Время окончания перерыва", default="12:00:00"
    )
    break_start_time = models.TimeField(
        verbose_name="Время начала перерыва", default="11:00:00"
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
    time_per_visit = models.IntegerField(
        default=Default.TIME_PER_VISIT_CHOICES[0][0],
        choices=Default.TIME_PER_VISIT_CHOICES,
    )
    arround_clock = models.BooleanField(
        default=False,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "расписание специалиста"

    def __str__(self):
        return f"{self.service} {self.weekday}"


class Slot(models.Model):
    """Слот для бронирования."""

    date = models.DateField(null=False, blank=False)
    time_from = models.TimeField(null=False, blank=False)
    time_to = models.TimeField(null=False, blank=False)
    supplier = models.ForeignKey(
        SupplierProfile,
        on_delete=models.CASCADE,
        related_name="slots",
    )

    class Meta:
        verbose_name = "слот бронирования"

    def __str__(self):
        return (
            f"Забронированно на {self.date} {self.time_from} - {self.time_to}"
        )
