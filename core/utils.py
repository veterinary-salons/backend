from core.models import Schedule
from services.models import Price


def update_schedules(schedules, schedules_data):
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
    existing_price_names = {price.service_name for price in prices}
    given_price_names = {
        price_data.get("service_name") for price_data in prices_data
    }

    to_delete_price_names = existing_price_names.difference(given_price_names)

    Price.objects.filter(
        service_name__in=to_delete_price_names, service=instance
    ).delete()
