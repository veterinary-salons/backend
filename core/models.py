from django.db import models
from django.db.models import CheckConstraint, Q, F

from core.constants import Default, Limits
from core.validators import RangeValueValidator
from services.models import Service
from users.models import SupplierProfile


class Schedule(models.Model):
    """Расписание услуги."""

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
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="schedules",
        null=False,
        blank=False,
    )
    class Meta:
        verbose_name = "расписание специалиста"


class Price(models.Model):
    """Стоимость услуги."""

    service_name = models.CharField(
        max_length=Limits.MAX_LEN_SERVICE_NAME,
    )
    cost_from = models.DecimalField(
        decimal_places=0,
        max_digits=5,
        default=Default.COST_FROM,
        validators=[RangeValueValidator(Limits.MIN_PRICE, Limits.MAX_PRICE)],
    )
    cost_to = models.DecimalField(
        decimal_places=0,
        max_digits=5,
        default=Default.COST_TO,
        validators=[RangeValueValidator(Limits.MIN_PRICE, Limits.MAX_PRICE)],
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    class Meta:
        verbose_name = "стоимость услуги"
        verbose_name_plural = "стоимости услуг"
        constraints = (
            CheckConstraint(
                check=Q(cost_from__lte=F("cost_to")),
                name="cost_range",
            ),
        )
