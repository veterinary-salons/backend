import datetime
import re

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, BaseValidator

from core.constants import Default, Messages, Limits


def validate_letters(value):
    if not re.match(r"^[a-zA-Zа-яА-Я]*$", value):
        raise ValidationError(
            "Поле должно содержать только русские и английские буквы."
        )


def validate_alphanumeric(value):
    if not re.match(r"^[a-zA-Zа-яА-Я0-9\s.,?!()-]*$", value):
        raise ValidationError(
            "Поле должно содержать только русские и английские буквы, цифры, "
            "знаки препинания и скобки."
        )


def validate_services(service_type, pet_type, task, formats, grooming_type):
    if service_type == Default.SERVICES[0][0] and pet_type != "dog":
        raise ValidationError("Кинолог работает только с собаками.")
    print(service_type, Default.SERVICES[0][0])
    if service_type != Default.SERVICES[0][0] and any(
        (
            task,
            formats,
        )
    ):
        print("Поля `task` и `formats` только для Сервиса")
        raise ValidationError("Поля `task` и `formats` только для Кинолога.")
    if service_type != Default.SERVICES[3][0] and grooming_type:
        raise ValidationError("Поле `grooming_type` только для Грумера.")
    if service_type == Default.SERVICES[3][0] and not grooming_type:
        raise ValidationError("Поле `grooming_type` необходимо заполнить.")
    if service_type == Default.SERVICES[0][0] and not all(
        (
            task,
            formats,
        )
    ):
        raise ValidationError("Поле `task` и `formats` необходимо заполнить.")


class RangeValueValidator(BaseValidator):
    def __init__(self, value_from, value_to):
        self.value_from = value_from
        self.value_to = value_to

    def __call__(self, value):
        if not self.value_from < value < self.value_to:
            raise ValidationError(
                f"Значение {value} должно быть в пределах от {self.value_from}"
                f" до {self.value_to}"
            )


def validate_current_and_future_month(value):
    current_month = datetime.date.today().month
    if value.month < current_month or value.month > current_month + 1:
        raise ValidationError(
            "Дата должна быть в текущем или следующем месяце."
        )
