from datetime import timedelta

from django.http import HttpRequest
from django.utils import timezone
from rest_framework import serializers

from users.models import CustomerProfile, SupplierProfile


def update_schedules(schedules, schedules_data):
    from core.models import Schedule
    for schedule in schedules:
        schedule_data = next(
            (
                item
                for item in schedules_data
                if item["weekday"] == schedule.weekday
            ),
            None,
        )
        schedule_update = []
        if schedule_data:
            schedule.weekday = schedule_data["weekday"]
            schedule.start_work_time = schedule_data["start_work_time"]
            schedule.end_work_time = schedule_data["end_work_time"]
            schedule.break_start_time = schedule_data["break_start_time"]
            schedule.break_end_time = schedule_data["break_end_time"]
            schedule.clean()
            schedule_update.append(schedule)
        Schedule.objects.bulk_update(
            schedule_update,
            [
                "service",
                "weekday",
                "start_work_time",
                "end_work_time",
                "break_start_time",
                "break_end_time",
            ],
        )


def create_schedules(instance, schedules_data):
    from core.models import Schedule
    existing_schedule_names = {
        schedule.weekday for schedule in instance.schedules.all()
    }
    given_schedule_names = {
        schedule_data.get("weekday") for schedule_data in schedules_data
    }
    to_create_schedule_names = given_schedule_names.difference(
        existing_schedule_names
    )
    for name in to_create_schedule_names:
        data = list(filter(lambda x: x.get("weekday") == name, schedules_data))
        schedule = Schedule(service=instance, **data[0])
        schedule.clean()
        schedule.save()


def delete_schedules(instance, schedules, schedules_data):
    from core.models import Schedule
    existing_schedule_names = {schedule.weekday for schedule in schedules}
    given_schedule_names = {
        schedule_data.get("weekday") for schedule_data in schedules_data
    }

    to_delete_schedule_names = existing_schedule_names.difference(
        given_schedule_names
    )

    Schedule.objects.filter(
        weekday__in=to_delete_schedule_names, service=instance
    ).delete()


def update_prices(prices, prices_data):
    from services.models import Price
    price_update = []
    for price in prices:
        price_data = next(
            (
                item
                for item in prices_data
                if item["service_name"] == price.service_name
            ),
            None,
        )
        if price_data:
            price.service_name = price_data["service_name"]
            price.cost_from = price_data["cost_from"]
            price.cost_to = price_data["cost_to"]
            price.clean()
            price_update.append(price)
    Price.objects.bulk_update(
        price_update, ["service_name", "cost_from", "cost_to"]
    )


def create_prices(instance, prices_data):
    from services.models import Price
    existing_price_names = {
        price.service_name for price in instance.prices.all()
    }
    given_price_names = {
        price_data.get("service_name") for price_data in prices_data
    }

    to_create_price_names = given_price_names.difference(existing_price_names)

    for name in to_create_price_names:
        data = list(
            filter(lambda x: x.get("service_name") == name, prices_data)
        )
        price = Price(service=instance, **data[0])
        price.clean()
        price.save()


def delete_prices(instance, prices, prices_data):
    """Удаление объекта `Price` из базы данных.

    Используется в случае, если в отредактированном списке объектов `Price`
    не оказалось объекта, который там был ранее. Этот объект будет удален.

    Args:
        instance: `Service` объект
        prices: список `Price`
        prices_data:

    Returns:

    """
    from services.models import Price
    existing_price_names = {price.service_name for price in prices}
    given_price_names = {
        price_data.get("service_name") for price_data in prices_data
    }

    to_delete_price_names = existing_price_names.difference(given_price_names)
    Price.objects.filter(
        service_name__in=to_delete_price_names, service=instance
    ).delete()


def get_customer(request):
    """Возвращает профиль заказчика для текущего пользователя.

    Если профиль не найден, возвращает 404 ошибку.

    Args:
        request: `HttpRequest` объект запроса

    Returns:
        `CustomerProfile` объект профиля поставщика
    """
    return get_object_or_404(CustomerProfile, related_user=request.user)


from django.shortcuts import get_object_or_404

def get_supplier(request):
    """Возвращает профиль исполнителя для текущего пользователя.

    Если профиль не найден, возвращает 404 ошибку.

    Args:
        request: `HttpRequest` объект запроса

    Returns:
        `SupplierProfile` объект профиля поставщика

    """
    return get_object_or_404(SupplierProfile, related_user=request.user)

def default_booking_time():
    """
        Возвращает текущее время плюс один день.

        Returns:
            Объект `datetime`, представляющий текущее время плюс один день.
    """
    return timezone.now() + timedelta(days=1)

def string_to_boolean(value:str) -> bool:
    """
        Преобразует строковое значение в булевое.
    Args:
        value: строка с булевым значением.

    Returns:
        Булевое значение.
    """
    if value is None:
        result = None
    elif value.lower() in ('true', "false"):
        result = value.lower() == "true"
    else:
        raise serializers.ValidationError('Value must be `true` or `false`')
    return result

