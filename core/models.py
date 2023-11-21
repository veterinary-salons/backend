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
    is_working_day = models.BooleanField(
        default=True, verbose_name="Рабочий день"
    )
    start_work_time = models.TimeField(
        verbose_name="Время начала работы", default="09:00:00"
    )
    end_work_time = models.TimeField(
        verbose_name="Время окончания работы", default="19:00:00"
    )


    class Meta:
        verbose_name = "расписание специалиста"

    def __str__(self):
        return f"{self.service} {self.weekday}"


class Slot(models.Model):
    """Слот для бронирования."""

    time_from = models.DateTimeField(null=False, blank=False)
    time_to = models.DateTimeField(null=False, blank=False)
    supplier = models.ForeignKey(
        SupplierProfile,
        on_delete=models.CASCADE,
        related_name="slots",
    )

    class Meta:
        verbose_name = "слот бронирования"

    def __str__(self):
        return (
            f"Забронированно на {self.time_from} {self.time_from} - {self.time_to}"
        )
